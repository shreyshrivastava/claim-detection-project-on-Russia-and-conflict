from claim_detection.data import load_default_evidence
from claim_detection.pipeline import analyze_claim


def test_pipeline_supported_case() -> None:
    result = analyze_claim(
        "The International Relief Mission delivered 20 generators to Northport hospital on Tuesday.",
        load_default_evidence(),
    )
    assert result.verdict == "supported"
    assert result.evidence[0].document.id == "doc-001"


def test_pipeline_refuted_case() -> None:
    result = analyze_claim(
        "The ceasefire corridor opened after midnight.",
        load_default_evidence(),
    )
    assert result.verdict == "refuted"
    assert result.evidence[0].document.id == "doc-008"


def test_pipeline_not_clear_claim_keeps_evidence_for_transparency() -> None:
    result = analyze_claim(
        "Did officials discuss the school repair grant?", load_default_evidence()
    )
    assert result.verdict == "not_a_clear_claim"
    assert result.evidence[0].document.id == "doc-004"


def test_pipeline_claim_without_evidence_is_insufficient() -> None:
    result = analyze_claim("The agency confirmed a repair grant on Monday.", [])
    assert result.verdict == "insufficient_evidence"
    assert result.confidence == 0.0
