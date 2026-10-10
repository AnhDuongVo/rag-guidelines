from types import SimpleNamespace

from rag_guidelines import verify


def test_mixed_valid_and_invalid_citations(monkeypatch):
    monkeypatch.setattr(
        verify, "by_id", lambda id: SimpleNamespace(text="HbA1c target below 7%.") if id == "ok" else None
    )
    report = verify.check_answer("HbA1c target below 7% [cite:ok] [cite:missing].")
    assert not report[0].supported and "not found" in report[0].reason


def test_unsupported_negation(monkeypatch):
    monkeypatch.setattr(verify, "by_id", lambda id: SimpleNamespace(text="Recommend metformin for diabetes."))
    report = verify.check_answer("Do not recommend metformin for diabetes [cite:ok].")
    assert not report[0].supported and "negation" in report[0].reason


def test_number_mismatch(monkeypatch):
    monkeypatch.setattr(verify, "by_id", lambda id: SimpleNamespace(text="HbA1c target below 7%."))
    assert not verify.check_answer("HbA1c target below 9% [cite:ok].")[0].supported
