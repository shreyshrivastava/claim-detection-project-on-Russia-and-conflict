"""Command-line interface for local claim analysis."""

from __future__ import annotations

import argparse
import json

from claim_detection.data import load_default_evidence, load_evidence_jsonl
from claim_detection.pipeline import analyze_claim


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim", required=True)
    parser.add_argument("--evidence-file", default="")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    evidence = (
        load_evidence_jsonl(args.evidence_file) if args.evidence_file else load_default_evidence()
    )
    result = analyze_claim(args.claim, evidence, top_k=args.top_k)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
