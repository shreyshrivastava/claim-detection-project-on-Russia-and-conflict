# Deployment to Vercel

The application is deployed on **Vercel** as a serverless Python function.

## How it Works (Demo Variant)

Due to Vercel's strict **50MB uncompressed size limit** for serverless functions, the original fine-tuned BERT model weights (~500MB) cannot be loaded directly in the cloud deployment. 

To overcome this, the **Vercel Demo Variant** is configured with an **LLM-augmented fail-safe**:
* It utilizes **`meta-llama/Llama-3.3-70B-Instruct`** via the Hugging Face Serverless Inference gateway.
* When a user queries a claim, the serverless function ranks matching evidence locally via TF-IDF, then sends the top documents to the 70B parameter Llama model to determine the final fact-check verdict and stance.
* This gateway is hosted publicly and is **100% free of charge** (requires no paid tokens or subscription).

## Local Deployment (Original BERT + SVM Model)

To run the exact fine-tuned BERT and Support Vector Classifier model from your dissertation locally:

1. Place your trained model files in the `artifacts/` folder:
   - `artifacts/svc_model.joblib`
   - `artifacts/bert_model.pth`
   - `artifacts/bert-base-uncased-tokenizer/` (Optional, defaults to download if not present)
2. Run the server locally:
   ```bash
   uvicorn claim_detection.api:app --reload
   ```
3. The server will automatically detect the files and switch to **Original BERT+SVM mode**.

## Environment Variables

* `HF_TOKEN`: Hugging Face API key to enable Llama 3.3 serverless fact checking (Free).
* `USE_MLX`: Set to `1` on Apple Silicon Macs to run the local Llama 3.2 3B model offline using MLX hardware acceleration.

## Cost Profile

* **0% Cost**: Hugging Face serverless provider endpoints do not charge for inference and do not require a credit card.
* **0% GPU Server Cost**: No need to host expensive GPU instances or pay monthly subscription fees.
