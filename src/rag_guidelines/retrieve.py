"""A small, dependency-free TF-IDF retriever over the corpus."""

from __future__ import annotations

import math
import re
from collections import Counter

from .corpus import CORPUS, Chunk

_TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class Retriever:
    def __init__(self, chunks: list[Chunk] | None = None):
        self.chunks = chunks or CORPUS
        self.docs = [tokenize(c.text) for c in self.chunks]
        n = len(self.docs)
        df: Counter[str] = Counter()
        for d in self.docs:
            df.update(set(d))
        self.idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
        self.vecs = [self._vec(d) for d in self.docs]

    def _vec(self, tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        return {t: (count / len(tokens)) * self.idf.get(t, 0.0) for t, count in tf.items()} if tokens else {}

    @staticmethod
    def _cos(a: dict[str, float], b: dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        num = sum(a[t] * b[t] for t in common)
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return num / (na * nb) if na and nb else 0.0

    def search(self, query: str, k: int = 3) -> list[tuple[Chunk, float]]:
        qv = self._vec(tokenize(query))
        scored = [(c, self._cos(qv, v)) for c, v in zip(self.chunks, self.vecs, strict=True)]
        scored.sort(key=lambda cs: cs[1], reverse=True)
        return [(c, s) for c, s in scored[:k] if s > 0]
