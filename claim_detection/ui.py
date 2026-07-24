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
          :root {
            color-scheme: light;
            --primary: #7b1f45;
            --on-primary: #ffffff;
            --primary-container: #ffd8e8;
            --on-primary-container: #32101f;
            --secondary: #4b6473;
            --secondary-container: #d3e8f4;
            --tertiary: #635b20;
            --tertiary-container: #ebe3a2;
            --error: #9f2f2f;
            --error-container: #ffdada;
            --surface: #fff8fb;
            --surface-container: #f4edf1;
            --surface-container-high: #ece3e8;
            --surface-container-highest: #e5dce1;
            --outline: #81737a;
            --outline-variant: #d4c2ca;
            --ink: #211a1e;
            --muted: #5f545a;
            --shadow: 0 14px 32px rgba(70, 42, 54, .12);
          }
          * { box-sizing: border-box; }
          body {
            margin: 0;
            min-height: 100vh;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background:
              radial-gradient(circle at top left, rgba(255, 216, 232, .72), transparent 34rem),
              linear-gradient(135deg, #fff8fb 0%, #f6f0f7 52%, #edf7fa 100%);
            color: var(--ink);
          }
          main {
            min-height: 100vh;
            display: grid;
            grid-template-columns: minmax(320px, 420px) minmax(0, 1fr);
          }
          aside {
            background: rgba(255, 248, 251, .72);
            border-right: 1px solid var(--outline-variant);
            padding: 32px;
            display: flex;
            flex-direction: column;
            gap: 18px;
            backdrop-filter: blur(18px);
          }
          .workspace {
            padding: 32px;
            display: grid;
            gap: 18px;
            align-content: start;
          }
          h1, h2, h3, p { margin-top: 0; }
          h1 {
            font-size: 38px;
            line-height: 1.04;
            margin-bottom: 4px;
            letter-spacing: 0;
          }
          h2 {
            font-size: 19px;
            line-height: 1.25;
            margin-bottom: 14px;
          }
          h3 {
            font-size: 16px;
            line-height: 1.3;
          }
          p {
            color: var(--muted);
            line-height: 1.58;
          }
          .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
          }
          .badge, .chip {
            width: fit-content;
            border-radius: 999px;
            padding: 7px 11px;
            font-size: 13px;
            font-weight: 800;
            border: 1px solid transparent;
          }
          .badge {
            background: var(--primary-container);
            color: var(--on-primary-container);
          }
          .chip {
            background: var(--secondary-container);
            color: #17313f;
          }
          .panel {
            background: rgba(255, 248, 251, .86);
            border: 1px solid var(--outline-variant);
            border-radius: 8px;
            padding: 20px;
            box-shadow: var(--shadow);
          }
          .tonal {
            background: var(--surface-container);
            box-shadow: none;
          }
          .warning {
            background: var(--tertiary-container);
            border: 1px solid #d4ca77;
            color: #252105;
            border-radius: 8px;
            padding: 13px 14px;
            font-weight: 700;
            line-height: 1.45;
          }
          .examples {
            display: grid;
            gap: 10px;
          }
          .example {
            text-align: left;
            border: 1px solid var(--outline-variant);
            background: var(--surface-container);
            color: var(--ink);
            border-radius: 8px;
            padding: 12px 14px;
            cursor: pointer;
            font: inherit;
            font-weight: 720;
            line-height: 1.35;
            transition: transform .14s ease, background .14s ease, border-color .14s ease;
          }
          .example:hover {
            transform: translateY(-1px);
            background: var(--primary-container);
            border-color: #d89ab4;
          }
          label {
            display: block;
            font-weight: 850;
            margin-bottom: 9px;
          }
          textarea {
            width: 100%;
            min-height: 136px;
            resize: vertical;
            border: 1px solid var(--outline);
            border-radius: 8px;
            padding: 15px;
            font: inherit;
            line-height: 1.48;
            background: #fff;
            color: var(--ink);
            outline-color: var(--primary);
          }
          .controls {
            display: flex;
            gap: 12px;
            align-items: center;
            flex-wrap: wrap;
            margin-top: 14px;
          }
          button.primary {
            background: var(--primary);
            color: var(--on-primary);
            border: 0;
            padding: 12px 18px;
            border-radius: 999px;
            font-weight: 850;
            cursor: pointer;
            box-shadow: 0 8px 18px rgba(123, 31, 69, .24);
          }
          button.primary:hover { background: #672039; }
          .status {
            min-height: 24px;
            color: var(--muted);
            font-weight: 700;
          }
          .summary {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
          }
          .metric {
            border: 1px solid var(--outline-variant);
            border-radius: 8px;
            padding: 14px;
            background: var(--surface-container);
          }
          .metric span {
            display: block;
            color: var(--muted);
            font-size: 12px;
            font-weight: 850;
            text-transform: uppercase;
          }
          .metric strong {
            display: block;
            margin-top: 6px;
            font-size: 23px;
            overflow-wrap: anywhere;
          }
          .evidence-list {
            display: grid;
            gap: 12px;
          }
          .evidence-card {
            border: 1px solid var(--outline-variant);
            border-left: 6px solid var(--primary);
            border-radius: 8px;
            padding: 15px;
            background: #fff;
          }
          .evidence-card.refuted { border-left-color: var(--error); }
          .evidence-card.uncertain { border-left-color: var(--tertiary); }
          .evidence-card.not_a_clear_claim { border-left-color: var(--secondary); }
          .card-head {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            align-items: start;
          }
          .card-head h3 { margin: 0; }
          .pill {
            border-radius: 999px;
            padding: 5px 10px;
            background: var(--primary-container);
            color: var(--on-primary-container);
            font-size: 12px;
            font-weight: 850;
            white-space: nowrap;
          }
          .evidence-card.refuted .pill {
            background: var(--error-container);
            color: #5c1111;
          }
          .evidence-card.uncertain .pill {
            background: var(--tertiary-container);
            color: #252105;
          }
          .evidence-card p { margin: 10px 0; }
          .rationale {
            margin: 8px 0 0;
            padding-left: 18px;
            color: var(--muted);
            line-height: 1.5;
          }
          .method-grid {
            display: grid;
            gap: 10px;
          }
          .method-item {
            background: var(--surface-container-high);
            border: 1px solid var(--outline-variant);
            border-radius: 8px;
            padding: 11px 12px;
          }
          .method-item strong {
            display: block;
            margin-bottom: 4px;
          }
          .error { color: var(--error); font-weight: 800; }
          @media (max-width: 900px) {
            main { grid-template-columns: 1fr; }
            aside { padding: 24px; border-right: 0; border-bottom: 1px solid var(--outline-variant); }
            .workspace { padding: 20px; }
            .summary { grid-template-columns: 1fr; }
            h1 { font-size: 32px; }
          }
        </style>
      </head>
      <body>
        <main>
          <aside>
            <div class="badge-row">
              <span class="badge">QMUL dissertation prototype</span>
              <span class="chip">Evidence screening</span>
            </div>
            <div>
              <h1>Claim Detection and Evidence Screening</h1>
              <p>A public demo derived from dissertation work on claim detection in conflict-related news. It screens a claim against example evidence and reports a cautious, reproducible result.</p>
            </div>
            <div class="warning">Research prototype only. This demo is not a professional fact-checking service, and the historical BERT/SVM artifacts are not included in this repository.</div>
            <section class="panel tonal">
              <h2>Try an example</h2>
              <div class="examples">
                <button class="example" data-claim="The International Relief Mission delivered 20 generators to Northport hospital on Tuesday.">Supported generator delivery</button>
                <button class="example" data-claim="The coastal power plant restarted full operations on Friday.">Refuted power-plant restart</button>
                <button class="example" data-claim="Did the satellite internet hub open yesterday?">Question, not a clear claim</button>
              </div>
            </section>
            <section class="method-grid">
              <div class="method-item"><strong>Current mode</strong><span>Deterministic demo using TF-IDF ranking and lexical stance screening.</span></div>
              <div class="method-item"><strong>Historical model</strong><span>BERT/SVM notebook outputs are documented as dissertation history, not reproduced here.</span></div>
            </section>
          </aside>
          <section class="workspace">
            <section class="panel">
              <label for="claim">Claim to screen</label>
              <textarea id="claim">The International Relief Mission delivered 20 generators to Northport hospital on Tuesday.</textarea>
              <div class="controls">
                <button class="primary" id="analyze">Analyze claim</button>
                <span class="status" id="status">Ready</span>
              </div>
            </section>
            <section class="panel" id="results">
              <h2>Result</h2>
              <p>Run the sample to see verdict, confidence, claim score, and ranked evidence cards.</p>
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
                body: JSON.stringify({ claim: claimBox.value })
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
                <h2 style="margin-top:18px">Ranked evidence</h2>
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
