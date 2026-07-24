import os
import pytest

@pytest.fixture(autouse=True)
def clear_hf_token(monkeypatch):
    """Automatically clear HF_TOKEN from environment for all tests to ensure deterministic runs."""
    monkeypatch.delenv("HF_TOKEN", raising=False)
