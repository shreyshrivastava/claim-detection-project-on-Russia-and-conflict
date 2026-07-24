from claim_detection.claim_detector import score_claim


def test_clear_event_claim_scores_as_claim() -> None:
    signal = score_claim(
        "The International Relief Mission delivered 20 generators to Northport hospital on Tuesday."
    )
    assert signal.is_claim
    assert signal.claim_score >= 0.7
    assert signal.features["has_number"] == 1
    assert signal.features["has_date"] == 1


def test_question_is_not_a_clear_claim() -> None:
    signal = score_claim("Did officials discuss the school repair grant?")
    assert not signal.is_claim
    assert signal.claim_score < 0.45


def test_hedging_terms_reduce_claim_certainty() -> None:
    direct = score_claim("The agency confirmed the hospital reopened on Monday.")
    hedged = score_claim("The agency reportedly confirmed the hospital may reopen on Monday.")
    assert direct.claim_score > hedged.claim_score
