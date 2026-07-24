"""Model service with an honest deterministic fallback."""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path

from claim_detection.config import ArtifactStatus, artifact_status
from claim_detection.evidence import rank_evidence
from claim_detection.pipeline import analyze_claim
from claim_detection.schemas import ClaimAnalysis, EvidenceDocument, EvidenceMatch


@dataclass(frozen=True)
class ModelServiceStatus:
    mode: str
    artifact_available: bool
    missing_artifacts: list[str]
    message: str


# Lazy load placeholders for local MLX model
_mlx_model = None
_mlx_tokenizer = None

# Lazy load placeholders for original BERT + SVM models
_original_tokenizer = None
_original_bert_model = None
_original_svc_model = None


def load_original_models(artifacts: ArtifactStatus) -> None:
    global _original_tokenizer, _original_bert_model, _original_svc_model
    if _original_svc_model is not None:
        return

    print("Loading original BERT + SVM models...")
    from transformers import AutoTokenizer, BertModel
    import torch
    import joblib
    from claim_detection.embeddings import get_device

    device = get_device()

    # Load tokenizer
    if artifacts.tokenizer_dir.exists():
        _original_tokenizer = AutoTokenizer.from_pretrained(str(artifacts.tokenizer_dir))
    else:
        _original_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    # Load BERT model
    _original_bert_model = BertModel.from_pretrained("bert-base-uncased").to(device)
    _original_bert_model.load_state_dict(torch.load(str(artifacts.bert_weights), map_location=device))
    _original_bert_model.eval()

    # Load SVC model
    _original_svc_model = joblib.load(str(artifacts.svm_model))
    print("Original models loaded successfully.")


def analyze_with_original_models(
    claim: str,
    documents: list[EvidenceDocument],
    artifacts: ArtifactStatus,
    top_k: int = 3,
) -> ClaimAnalysis:
    import numpy as np
    from sklearn.preprocessing import normalize
    from scipy.special import expit
    from claim_detection.embeddings import get_device, bert_cls_embeddings

    load_original_models(artifacts)
    device = get_device()

    # 1. Get embedding for the claim
    claim_emb = bert_cls_embeddings([claim], tokenizer=_original_tokenizer, bert_model=_original_bert_model, device=device)
    claim_emb_norm = normalize(claim_emb)

    # 2. Get embeddings for evidence documents
    doc_texts = [f"{doc.title} {doc.text}" for doc in documents]
    doc_embs = bert_cls_embeddings(doc_texts, tokenizer=_original_tokenizer, bert_model=_original_bert_model, device=device)
    doc_embs_norm = normalize(doc_embs)

    # 3. Calculate similarity
    similarities = np.dot(claim_emb_norm, doc_embs_norm.T).flatten()

    # 4. Rank documents
    ranked_indexes = np.argsort(similarities)[::-1][:top_k]

    # 5. Classify stance for each ranked document using the SVM
    matches: list[EvidenceMatch] = []

    for idx in ranked_indexes:
        doc = documents[int(idx)]
        similarity = float(similarities[int(idx)])

        from claim_detection.evidence import _overlap_ratio
        overlap = _overlap_ratio(claim, f"{doc.title} {doc.text}")

        combined_text = f"{claim} {doc.title} {doc.text}"
        combined_emb = bert_cls_embeddings([combined_text], tokenizer=_original_tokenizer, bert_model=_original_bert_model, device=device)

        decision_score = _original_svc_model.decision_function(combined_emb)[0]
        prob_supported = float(expit(decision_score))

        if prob_supported >= 0.5:
            stance = "supported"
            rationale = [f"SVM classified combined representation as Supported (probability: {prob_supported:.4f})"]
        else:
            stance = "refuted"
            rationale = [f"SVM classified combined representation as Refuted (probability: {1.0 - prob_supported:.4f})"]

        matches.append(
            EvidenceMatch(
                document=doc,
                similarity=round(similarity, 4),
                overlap_ratio=round(overlap, 4),
                stance=stance,
                rationale=rationale,
            )
        )

    from claim_detection.claim_detector import score_claim
    signal = score_claim(claim)

    if not matches:
        verdict = "insufficient_evidence"
        overall_conf = 0.0
    else:
        if not signal.is_claim:
            verdict = "not_a_clear_claim"
            overall_conf = round(max(0.0, 1 - signal.claim_score), 4)
        else:
            verdict = matches[0].stance
            overall_conf = round(matches[0].similarity, 4)

    return ClaimAnalysis(
        claim=claim,
        signal=signal,
        verdict=verdict,
        confidence=overall_conf,
        evidence=matches,
        limitations=[
            "Classification and ranking generated via the original fine-tuned BERT + SVM models.",
            "Local matches ranked via BERT embedding cosine similarity."
        ],
    )


def query_mlx_llm(claim: str, documents: list[EvidenceDocument]) -> dict[str, object] | None:
    global _mlx_model, _mlx_tokenizer
    try:
        import mlx_lm
    except ImportError:
        return None

    model_id = "mlx-community/Llama-3.2-3B-Instruct-4bit"

    if _mlx_model is None:
        print(f"Loading local MLX model {model_id}...")
        _mlx_model, _mlx_tokenizer = mlx_lm.load(model_id)
        print("Local MLX model loaded successfully.")

    evidence_text = ""
    for idx, doc in enumerate(documents, 1):
        evidence_text += f"Document {idx} (Source: {doc.source}):\nTitle: {doc.title}\nText: {doc.text}\n\n"

    system_prompt = (
        "You are a fact-checker. Respond in valid JSON only. "
        "The JSON object must have keys: "
        "verdict (must be exactly one of: supported, refuted, uncertain, insufficient_evidence, not_a_clear_claim), "
        "confidence (float between 0.0 and 1.0), "
        "rationale (list of strings explaining the reasoning)."
    )
    user_prompt = f"Claim: {claim}\n\nEvidence:\n{evidence_text}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        prompt = _mlx_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        response = mlx_lm.generate(_mlx_model, _mlx_tokenizer, prompt=prompt, verbose=False, max_tokens=256)
        
        clean_response = response.strip()
        if "```json" in clean_response:
            clean_response = clean_response.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_response:
            clean_response = clean_response.split("```")[1].split("```")[0].strip()

        parsed_content = json.loads(clean_response)
        return parsed_content
    except Exception as e:
        print(f"Local MLX LLM generation/parsing error: {e}")
        return None


def query_hf_llm(claim: str, documents: list[EvidenceDocument]) -> dict[str, object] | None:
    token = os.getenv("HF_TOKEN")
    if not token:
        return None

    url = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    evidence_text = ""
    for idx, doc in enumerate(documents, 1):
        evidence_text += f"Document {idx} (Source: {doc.source}):\nTitle: {doc.title}\nText: {doc.text}\n\n"

    payload = {
        "model": "meta-llama/Llama-3.3-70B-Instruct",
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a fact-checker. Respond in valid JSON only. "
                    "The JSON object must have keys: "
                    "verdict (must be exactly one of: supported, refuted, uncertain, insufficient_evidence, not_a_clear_claim), "
                    "confidence (float between 0.0 and 1.0), "
                    "rationale (list of strings explaining the reasoning)."
                )
            },
            {
                "role": "user",
                "content": f"Claim: {claim}\n\nEvidence:\n{evidence_text}"
            }
        ]
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=5.0) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            assistant_message = res_json["choices"][0]["message"]["content"]
            parsed_content = json.loads(assistant_message)
            return parsed_content
    except Exception as e:
        print(f"HF Inference API error: {e}")
        return None


class ClaimModelService:
    """Serve claim analysis supporting original BERT+SVM models, MLX LLMs, and cloud LLMs."""

    def __init__(self, artifacts: ArtifactStatus | None = None) -> None:
        self.artifacts = artifacts or artifact_status()

    @property
    def status(self) -> ModelServiceStatus:
        if self.artifacts.available:
            return ModelServiceStatus(
                mode="original_bert_svm",
                artifact_available=True,
                missing_artifacts=[],
                message="Running in original BERT + SVM mode (QMUL dissertation model loaded).",
            )

        has_mlx = False
        try:
            import mlx_lm
            has_mlx = True
        except ImportError:
            pass

        if os.getenv("USE_MLX") == "1" and has_mlx:
            return ModelServiceStatus(
                mode="local_mlx_llm",
                artifact_available=True,
                missing_artifacts=[],
                message="Running in local MLX-augmented mode powered by Llama 3.2 3B (Offline).",
            )
        if os.getenv("HF_TOKEN"):
            return ModelServiceStatus(
                mode="hybrid_llm_augmented",
                artifact_available=True,
                missing_artifacts=[],
                message="Running in hybrid LLM-augmented mode powered by meta-llama/Llama-3.3-70B-Instruct.",
            )

        return ModelServiceStatus(
            mode="deterministic_demo",
            artifact_available=False,
            missing_artifacts=self.artifacts.missing,
            message=(
                "Historical BERT/SVM artifacts are not available; using deterministic "
                "claim screening, evidence ranking, and stance heuristics."
            ),
        )

    def analyze(
        self,
        claim: str,
        documents: list[EvidenceDocument],
        *,
        top_k: int = 3,
    ) -> ClaimAnalysis:
        # 1. If original BERT + SVM artifacts are available, run using the original model
        if self.artifacts.available:
            try:
                return analyze_with_original_models(claim, documents, self.artifacts, top_k=top_k)
            except Exception as e:
                print(f"Failed to analyze using original BERT+SVM: {e}")

        # 2. Check for LLM modes or fallback to deterministic
        ranked_matches = rank_evidence(claim, documents, top_k=top_k)

        has_mlx = False
        try:
            import mlx_lm
            has_mlx = True
        except ImportError:
            pass

        llm_analysis = None
        mode_used = "deterministic"

        if os.getenv("USE_MLX") == "1" and has_mlx and ranked_matches:
            top_docs = [m.document for m in ranked_matches]
            llm_analysis = query_mlx_llm(claim, top_docs)
            mode_used = "local_mlx"
        elif os.getenv("HF_TOKEN") and ranked_matches:
            top_docs = [m.document for m in ranked_matches]
            llm_analysis = query_hf_llm(claim, top_docs)
            mode_used = "hybrid_llm"

        if llm_analysis:
            try:
                verdict = llm_analysis.get("verdict")
                if verdict not in ["supported", "refuted", "uncertain", "insufficient_evidence", "not_a_clear_claim"]:
                    verdict = "uncertain"

                confidence = float(llm_analysis.get("confidence", 0.5))
                rationale = list(llm_analysis.get("rationale", []))

                from claim_detection.claim_detector import score_claim
                signal = score_claim(claim)

                if ranked_matches:
                    ranked_matches[0] = ranked_matches[0].__class__(
                        document=ranked_matches[0].document,
                        similarity=ranked_matches[0].similarity,
                        overlap_ratio=ranked_matches[0].overlap_ratio,
                        stance=verdict,
                        rationale=rationale
                    )

                limitations = [
                    "Local matches ranked via TF-IDF overlap."
                ]
                if mode_used == "local_mlx":
                    limitations.insert(0, "Local MLX-augmented screening powered by Llama 3.2 3B (Offline).")
                else:
                    limitations.insert(0, "Hybrid LLM-augmented screening powered by Llama 3.3 70B.")

                return ClaimAnalysis(
                    claim=claim,
                    signal=signal,
                    verdict=verdict,
                    confidence=confidence,
                    evidence=ranked_matches,
                    limitations=limitations,
                )
            except Exception:
                pass

        return analyze_claim(claim, documents, top_k=top_k)

    def rank(
        self,
        claim: str,
        documents: list[EvidenceDocument],
        *,
        top_k: int = 3,
    ):
        return rank_evidence(claim, documents, top_k=top_k)
