"""FastAPI app for claim evidence screening."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from claim_detection.data import load_default_evidence
from claim_detection.model import ClaimModelService
from claim_detection.schemas import EvidenceDocument
from claim_detection.ui import render_index

app = FastAPI(
    title="Claim Evidence Checker",
    description="Deterministic claim screening and evidence ranking demo.",
    version="1.0.0",
)

model_service = ClaimModelService()


class EvidencePayload(BaseModel):
    id: str
    title: str
    text: str
    source: str = "request"
    published_at: str | None = None


class AnalyzeRequest(BaseModel):
    claim: str = Field(..., min_length=3, max_length=1000)
    evidence: list[EvidencePayload] | None = None
    top_k: int = Field(default=3, ge=1, le=10)


@app.get("/health")
def health() -> dict[str, object]:
    service_status = model_service.status
    return {
        "status": "healthy",
        "app": "claim-evidence-checker",
        "mode": service_status.mode,
        "artifact_available": service_status.artifact_available,
        "missing_artifacts": service_status.missing_artifacts,
    }


@app.post("/analyze")
def analyze(payload: AnalyzeRequest) -> dict[str, object]:
    documents = (
        [
            EvidenceDocument(
                id=item.id,
                title=item.title,
                text=item.text,
                source=item.source,
                published_at=item.published_at,
            )
            for item in payload.evidence
        ]
        if payload.evidence
        else load_default_evidence()
    )
    return model_service.analyze(payload.claim, documents, top_k=payload.top_k).to_dict()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return render_index()
