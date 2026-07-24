# Deployment

Render is the recommended host for the current version because the app is a Dockerized FastAPI service. It does not require Streamlit, GPUs, API keys, model downloads, or persistent storage.

## Render Blueprint

1. Push the branch containing `render.yaml` and `Dockerfile`.
2. In Render, create a new Blueprint from the GitHub repository.
3. Select the `claim-evidence-checker` service.
4. Use the free plan unless traffic requirements change.
5. Confirm the health check path is `/health`.
6. After deployment, verify:

```bash
curl https://YOUR_RENDER_SERVICE.onrender.com/health
```

Expected response:

```json
{"status":"healthy","app":"claim-evidence-checker","mode":"deterministic"}
```

## Cost Profile

- No paid LLM or search APIs.
- No hosted model inference.
- No GPU requirement.
- Free Render services can cold start after inactivity.

## Production Hardening Still Needed

- Add persistent observability if the service receives real users.
- Add request throttling if abuse becomes likely.
- Replace synthetic evidence with a managed evidence store before making factual claims.
- Reproduce and audit the BERT/SVM model before deploying learned predictions.
