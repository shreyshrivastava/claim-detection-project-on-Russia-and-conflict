"""Backward-compatible wrapper for the leakage audit.

Import from `evaluation.leakage_audit` in new code.
"""

from evaluation.leakage_audit import *  # noqa: F403
from evaluation.leakage_audit import main

if __name__ == "__main__":
    main()
