"""FastAPI app for claim evidence screening."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from claim_detection.data import load_default_evidence
from claim_detection.pipeline import analyze_claim
from claim_detection.schemas import EvidenceDocument

app = FastAPI(
    title="Claim Evidence Checker",
    description="Deterministic claim screening and evidence ranking demo.",
    version="1.0.0",
)


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
def health() -> dict[str, str]:
    return {"status": "healthy", "app": "claim-evidence-checker", "mode": "deterministic"}


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
    return analyze_claim(payload.claim, documents, top_k=payload.top_k).to_dict()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Claim Evidence Checker</title>
        <style>
          body { font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: #f8fafc; color: #111827; }
          main { max-width: 1040px; margin: 0 auto; padding: 42px 24px; }
          h1 { font-size: 40px; margin: 0 0 8px; }
          p { color: #475569; line-height: 1.6; }
          .panel { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin-top: 22px; }
          textarea { width: 100%; min-height: 110px; border: 1px solid #cbd5e1; border-radius: 6px; padding: 12px; font: inherit; box-sizing: border-box; }
          button { background: #0f766e; color: white; border: 0; padding: 11px 16px; border-radius: 6px; font-weight: 700; cursor: pointer; margin-top: 12px; }
          pre { background: #0f172a; color: #e2e8f0; padding: 16px; border-radius: 6px; overflow: auto; }
          .warning { background: #fff7ed; border: 1px solid #fed7aa; color: #9a3412; padding: 12px; border-radius: 6px; }
        </style>
      </head>
      <body>
        <main>
          <h1>Claim Evidence Checker</h1>
          <p>Deterministic claim-likelihood screening, evidence retrieval, and coarse stance classification.</p>
          <div class="warning">Portfolio demo only. This is not a professional fact-checking system.</div>
          <section class="panel">
            <label for="claim"><strong>Claim</strong></label>
            <textarea id="claim">The International Relief Mission delivered 20 generators to Northport hospital on Tuesday.</textarea>
            <button onclick="analyze()">Analyze claim</button>
          </section>
          <section class="panel">
            <h2>Result</h2>
            <pre id="result">Click Analyze claim to run the deterministic sample.</pre>
          </section>
        </main>
        <script>
          async function analyze() {
            const claim = document.getElementById("claim").value;
            const response = await fetch("/analyze", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({ claim })
            });
            const data = await response.json();
            document.getElementById("result").textContent = JSON.stringify(data, null, 2);
          }
        </script>
      </body>
    </html>
    """
