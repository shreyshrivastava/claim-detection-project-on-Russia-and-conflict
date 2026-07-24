"""HTML UI for the FastAPI demo."""

from __future__ import annotations


def render_index() -> str:
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Claim Evidence Checker</title>
        <style>
          :root { color-scheme: light; --ink:#17202a; --muted:#5b6675; --line:#d9e1ea; --panel:#ffffff; --accent:#0b6f6b; --accent-dark:#084e4b; --warn:#8a4b08; --warn-bg:#fff8e8; --ok:#176b3a; --bad:#9f2f2f; }
          * { box-sizing: border-box; }
          body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #eef3f6; color: var(--ink); }
          main { min-height: 100vh; display: grid; grid-template-columns: minmax(320px, 430px) minmax(0, 1fr); }
          aside { background: #14343c; color: #f7fbfc; padding: 34px 30px; display: flex; flex-direction: column; gap: 22px; }
          h1 { font-size: 34px; line-height: 1.05; margin: 0; letter-spacing: 0; }
          h2 { font-size: 18px; margin: 0 0 12px; }
          p { color: var(--muted); line-height: 1.55; }
          aside p { color: #d4e3e7; margin: 0; }
          .badge { display: inline-flex; width: fit-content; border: 1px solid #81b8b6; color: #e4fffd; border-radius: 999px; padding: 6px 10px; font-size: 13px; font-weight: 700; }
          .examples { display: grid; gap: 10px; }
          .example { text-align: left; border: 1px solid rgba(255,255,255,.22); background: rgba(255,255,255,.07); color: #f7fbfc; border-radius: 8px; padding: 10px 12px; cursor: pointer; font: inherit; }
          .workspace { padding: 34px; display: grid; gap: 18px; align-content: start; }
          .panel { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 20px; box-shadow: 0 10px 24px rgba(30, 45, 55, .06); }
          label { display:block; font-weight: 800; margin-bottom: 8px; }
          textarea { width: 100%; min-height: 128px; resize: vertical; border: 1px solid #b8c6d4; border-radius: 8px; padding: 13px 14px; font: inherit; line-height: 1.45; background: #fbfdfe; color: var(--ink); }
          .controls { display:flex; gap: 12px; align-items:center; flex-wrap:wrap; margin-top: 13px; }
          button.primary { background: var(--accent); color: white; border: 0; padding: 11px 15px; border-radius: 8px; font-weight: 800; cursor: pointer; }
          button.primary:hover { background: var(--accent-dark); }
          .status { min-height: 24px; color: var(--muted); }
          .warning { background: var(--warn-bg); border: 1px solid #f1cf91; color: var(--warn); padding: 12px 14px; border-radius: 8px; font-weight: 650; }
          .summary { display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 12px; }
          .metric { border: 1px solid var(--line); border-radius: 8px; padding: 13px; background:#fbfdfe; }
          .metric span { display:block; color: var(--muted); font-size: 12px; font-weight: 800; text-transform: uppercase; }
          .metric strong { display:block; margin-top: 6px; font-size: 22px; overflow-wrap: anywhere; }
          .evidence-list { display:grid; gap: 12px; }
          .evidence-card { border: 1px solid var(--line); border-left: 5px solid var(--accent); border-radius: 8px; padding: 14px; background:#fff; }
          .evidence-card.refuted { border-left-color: var(--bad); }
          .evidence-card.uncertain { border-left-color: #76621a; }
          .card-head { display:flex; justify-content:space-between; gap:12px; align-items:start; }
          .card-head h3 { margin:0; font-size: 16px; }
          .pill { border-radius: 999px; padding: 4px 9px; background:#eef5f5; color: var(--accent-dark); font-size: 12px; font-weight:800; white-space: nowrap; }
          .evidence-card p { margin: 9px 0; }
          .rationale { margin: 8px 0 0; padding-left: 18px; color: var(--muted); }
          .error { color: #8f1d1d; font-weight: 700; }
          @media (max-width: 820px) { main { grid-template-columns: 1fr; } aside { padding: 24px; } .workspace { padding: 20px; } .summary { grid-template-columns: 1fr; } }
        </style>
      </head>
      <body>
        <main>
          <aside>
            <span class="badge">MSc Dissertation Project</span>
            <h1>Claim Evidence Checker</h1>
            <p>A dissertation project at <strong>Queen Mary University of London</strong> that turns notebook-era BERT/SVM claim-detection research into a tested FastAPI evidence-ranking and stance-screening pipeline. Enter a factual claim and compare it with evidence snippets.</p>
            <p style="margin-top:6px"><a href="https://claim-detection-project.vercel.app" style="color:#81d4cf;text-decoration:underline">Live on Vercel →</a></p>
            <div class="warning">Academic dissertation demo. Note: The original BERT model (~500MB) is too large for serverless cloud deployment (Vercel has a 50MB size limit). The live demo uses a high-accuracy Llama 3.3 70B LLM (via Hugging Face) as a fail-safe, which is completely free of cost.</div>
            <section>
              <h2>Examples</h2>
              <div class="examples">
                <button class="example" data-claim="The International Relief Mission delivered 20 generators to Northport hospital on Tuesday.">Supported generator delivery</button>
                <button class="example" data-claim="The coastal power plant restarted full operations on Friday.">Refuted power-plant restart</button>
                <button class="example" data-claim="Did the satellite internet hub open yesterday?">Question, not a clear claim</button>
              </div>
            </section>
          </aside>
          <section class="workspace">
            <section class="panel">
              <label for="claim">Claim</label>
              <textarea id="claim">The International Relief Mission delivered 20 generators to Northport hospital on Tuesday.</textarea>
              <div style="margin: 14px 0; display: flex; align-items: center; gap: 8px;">
                <input type="checkbox" id="use_rss" style="width: 18px; height: 18px; cursor: pointer; margin: 0;" />
                <label for="use_rss" style="margin: 0; cursor: pointer; font-weight: 500; font-size: 14px; color: var(--muted);">Use Live RSS Conflict & World News feeds (Real-time detection)</label>
              </div>
              <div class="controls">
                <button class="primary" id="analyze">Analyze claim</button>
                <span class="status" id="status">Ready</span>
              </div>
            </section>
            <section class="panel" id="results">
              <h2>Result</h2>
              <p>Run the sample to see verdict, confidence, and ranked evidence cards.</p>
            </section>
          </section>
        </main>
        <script>
          const claimBox = document.getElementById("claim");
          const statusEl = document.getElementById("status");
          const results = document.getElementById("results");
          document.querySelectorAll(".example").forEach((button) => {
            button.addEventListener("click", () => { claimBox.value = button.dataset.claim; run(); });
          });
          document.getElementById("analyze").addEventListener("click", run);
          function fmt(value) { return typeof value === "number" ? value.toFixed(3) : value; }
          function escapeHtml(text) {
            return String(text).replace(/[&<>"']/g, (m) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;" }[m]));
          }
          async function run() {
            statusEl.textContent = "Analyzing...";
            results.innerHTML = "<h2>Result</h2><p>Ranking evidence and screening stance...</p>";
            try {
              const response = await fetch("/analyze", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                  claim: claimBox.value,
                  use_rss: document.getElementById("use_rss").checked
                })
              });
              if (!response.ok) throw new Error("Request failed with status " + response.status);
              const data = await response.json();
              statusEl.textContent = "Complete";
              const cards = data.evidence.map((item) => `
                <article class="evidence-card ${escapeHtml(item.stance)}">
                  <div class="card-head">
                    <h3>${escapeHtml(item.document.title)}</h3>
                    <span class="pill">${escapeHtml(item.stance)}</span>
                  </div>
                  <p>${escapeHtml(item.document.text)}</p>
                  <p><strong>Similarity:</strong> ${fmt(item.similarity)} &nbsp; <strong>Overlap:</strong> ${fmt(item.overlap_ratio)}</p>
                  <ul class="rationale">${item.rationale.map((r) => `<li>${escapeHtml(r)}</li>`).join("")}</ul>
                </article>`).join("");
              results.innerHTML = `
                <h2>Result</h2>
                <div class="summary">
                  <div class="metric"><span>Verdict</span><strong>${escapeHtml(data.verdict)}</strong></div>
                  <div class="metric"><span>Confidence</span><strong>${fmt(data.confidence)}</strong></div>
                  <div class="metric"><span>Claim score</span><strong>${fmt(data.signal.claim_score)}</strong></div>
                </div>
                <h2 style="margin-top:18px">Ranked Evidence</h2>
                <div class="evidence-list">${cards || "<p>No evidence returned.</p>"}</div>
                <h2 style="margin-top:18px">Limitations</h2>
                <ul class="rationale">${data.limitations.map((r) => `<li>${escapeHtml(r)}</li>`).join("")}</ul>`;
            } catch (err) {
              statusEl.textContent = "Error";
              results.innerHTML = `<h2>Result</h2><p class="error">${escapeHtml(err.message)}</p>`;
            }
          }
        </script>
      </body>
    </html>
    """
