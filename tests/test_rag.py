"""Retrieval finds the right chunk; verification passes grounded answers and flags bad ones."""

from __future__ import annotations

from rag_guidelines.generate import generate_offline
from rag_guidelines.retrieve import Retriever
from rag_guidelines.verify import check_answer, summary


def test_retrieval_finds_relevant_chunk():
    hits = Retriever().search("what is the maximum metformin dose?", k=3)
    assert hits
    assert hits[0][0].id == "met-1"


def test_offline_answer_is_grounded():
    hits = Retriever().search("maximum metformin dose", k=2)
    ans = generate_offline("maximum metformin dose", hits)
    checks = check_answer(ans)
    assert checks and all(c.supported for c in checks)
    assert summary(checks)["supported_rate"] == 1.0


def test_verify_flags_unsupported_number():
    # a fabricated dose cited to a real chunk should be flagged (number not in source)
    bad = "The maximum metformin dose is 9999 mg per day [cite:met-1]."
    checks = check_answer(bad)
    assert checks and not checks[0].supported


def test_verify_flags_missing_citation():
    checks = check_answer("Metformin is first line.")
    assert checks and not checks[0].supported and checks[0].reason == "no citation"
