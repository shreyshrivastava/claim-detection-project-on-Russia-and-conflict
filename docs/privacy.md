# Privacy

## Data Processed

The app processes:

- user-submitted claim text
- optional evidence text supplied in the API request
- built-in synthetic evidence fixtures when no evidence is supplied

Optional RSS ingestion fetches public RSS feed entries from configured URLs.

## Storage

The application does not store claim text, evidence text, uploaded files, or user identifiers. Evaluation and benchmark scripts write only synthetic results generated from repository fixtures.

## Logging

FastAPI, Uvicorn, and Vercel may log request metadata such as method, path, status code, timestamps, and client network metadata. The application does not intentionally log request bodies.

## External Services

The deterministic API does not call paid APIs or hosted AI services. Optional RSS ingestion makes HTTP requests to public feed URLs only when explicitly used.

## Sensitive Content

Do not submit private documents, personal data, confidential claims, or legally sensitive material to a public demo. The system is not a verified fact-checking service.
