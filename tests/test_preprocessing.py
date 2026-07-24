from claim_detection.preprocessing import normalize_text, split_sentences, tokenize


def test_normalize_text_removes_urls_and_collapses_whitespace() -> None:
    assert normalize_text("Alpha   https://example.com/x\nBeta") == "Alpha Beta"


def test_split_sentences_handles_empty_and_punctuation() -> None:
    assert split_sentences("") == []
    assert split_sentences("One claim. Another question? Final.") == [
        "One claim.",
        "Another question?",
        "Final.",
    ]


def test_tokenize_lowercases_and_removes_stopwords_by_default() -> None:
    assert tokenize("The Relief Mission delivered generators") == [
        "relief",
        "mission",
        "delivered",
        "generators",
    ]


def test_tokenize_can_keep_stopwords() -> None:
    assert "the" in tokenize("The report was signed", remove_stopwords=False)
