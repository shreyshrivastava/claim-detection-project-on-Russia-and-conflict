import pytest

from claim_detection.data import load_default_evidence
from claim_detection.evidence import rank_evidence


def test_rank_evidence_returns_expected_top_fixture() -> None:
    matches = rank_evidence(
        "The coastal power plant restarted full operations on Friday.",
        load_default_evidence(),
    )
    assert matches[0].document.id == "doc-002"
    assert matches[0].stance == "refuted"


def test_rank_evidence_handles_empty_inputs() -> None:
    assert rank_evidence("", load_default_evidence()) == []
    assert rank_evidence("A claim", []) == []


def test_rank_evidence_rejects_invalid_top_k() -> None:
    with pytest.raises(ValueError, match="top_k"):
        rank_evidence("A claim", load_default_evidence(), top_k=0)
