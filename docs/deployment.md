# Deployment

Vercel is the target host for the public dissertation demo. The app uses Vercel's Python runtime to serve the existing FastAPI application from `api/index.py`.

The deployment is intentionally CPU-only and does not require paid APIs, GPUs, private datasets, model downloads, or secrets.

## Vercel Setup

1. Push the branch containing `vercel.json` and `api/index.py`.
2. In Vercel, import the GitHub repository.
3. Keep the project root at the repository root.
4. Let Vercel install `requirements.txt`.
5. Deploy the project.
6. After deployment, verify:

```bash
curl https://YOUR_VERCEL_PROJECT.vercel.app/health
```

Expected response:

```json
{
  "status": "healthy",
  "app": "claim-evidence-checker",
  "mode": "deterministic_demo",
  "artifact_available": false,
  "missing_artifacts": [".../artifacts/svm_model.joblib", "..."]
}
```

## Vercel Files

- `vercel.json`: routes all requests to the Python FastAPI function.
- `api/index.py`: imports the FastAPI `app` from `claim_detection.api`.
- `runtime.txt`: pins Python 3.12 for hosting compatibility.

## Cost Profile

- No paid LLM or search APIs.
- No hosted model inference.
- No GPU requirement.
- No persistent database or object storage requirement.

## Production Hardening Still Needed

- Add persistent observability if the service receives real users.
- Add request throttling if abuse becomes likely.
- Replace synthetic evidence with a managed evidence store before making factual claims.
- Reproduce and audit the BERT/SVM model before deploying learned predictions.
