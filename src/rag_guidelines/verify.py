"""Citation verification: citation integrity plus lexical/numerical screening, not semantic entailment.

A sentence is supported when the chunk it cites exists, enough of the sentence's content words appear in that
chunk, and every number in the sentence appears in the chunk. Unsupported sentences are flagged.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from .corpus import by_id
from .retrieve import tokenize

_CITE = re.compile(r"\[cite:([a-z0-9-]+)\]", re.I)
_NUM = re.compile(r"-?\d+(?:\.\d+)?")
_STOP = {
    "the",
    "a",
    "an",
    "of",
    "for",
    "and",
    "or",
    "to",
    "in",
    "is",
    "are",
    "with",
    "at",
    "below",
    "above",
    "when",
    "than",
    "that",
    "this",
}


@dataclass
class SentenceCheck:
    sentence: str
    cited: list[str]
    supported: bool
    reason: str


def _content(tokens: list[str]) -> set[str]:
    return {t for t in tokens if t not in _STOP}


def check_answer(answer: str, overlap_threshold: float = 0.6) -> list[SentenceCheck]:
    checks: list[SentenceCheck] = []
    for raw in re.split(r"(?<=[.!?])\s+", answer.strip()):
        if not raw.strip():
            continue
        cited = _CITE.findall(raw)
        clean = _CITE.sub("", raw).strip()
        if not cited:
            checks.append(SentenceCheck(clean, [], False, "no citation"))
            continue
        chunks = [by_id(c) for c in cited]
        if any(c is None for c in chunks):
            checks.append(SentenceCheck(clean, cited, False, "cited id not found"))
            continue
        source_text = " ".join(c.text for c in chunks)
        sent_tokens = _content(tokenize(clean))
        chunk_tokens = set(tokenize(source_text))
        overlap = len(sent_tokens & chunk_tokens) / len(sent_tokens) if sent_tokens else 0.0
        nums = set(_NUM.findall(clean))
        chunk_nums = set(_NUM.findall(source_text))
        missing_nums = nums - chunk_nums
        neg = r"\b(?:no|not|never|without|avoid|contraindicated)\b"
        if bool(re.search(neg, clean, re.I)) != bool(re.search(neg, source_text, re.I)):
            checks.append(SentenceCheck(clean, cited, False, "negation differs; semantic review required"))
        elif missing_nums:
            checks.append(SentenceCheck(clean, cited, False, f"number(s) not in source: {sorted(missing_nums)}"))
        elif overlap >= overlap_threshold:
            checks.append(SentenceCheck(clean, cited, True, f"lexical screen passed (overlap {overlap:.0%})"))
        else:
            checks.append(SentenceCheck(clean, cited, False, f"weak support (overlap {overlap:.0%})"))
    return checks


def summary(checks: list[SentenceCheck]) -> dict:
    n = len(checks)
    ok = sum(c.supported for c in checks)
    return {"sentences": n, "supported": ok, "supported_rate": ok / n if n else None}
