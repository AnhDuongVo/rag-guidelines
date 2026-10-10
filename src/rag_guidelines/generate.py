"""Answer generation. Offline by default (extractive, always grounded); live via any OpenAI-compatible API."""

from __future__ import annotations

from .config import Settings
from .corpus import Chunk

SYSTEM = (
    "You answer clinical questions ONLY from the provided context. Cite the id of every chunk you use as "
    "[cite:<id>] right after the sentence it supports. If the context does not answer the question, say so."
)


def _context(chunks: list[Chunk]) -> str:
    return "\n".join(f"[{c.id}] {c.text}" for c in chunks)


def generate_offline(question: str, chunks: list[tuple[Chunk, float]]) -> str:
    """Extractive, always-grounded answer: restate the top chunks, each with its citation."""
    if not chunks:
        return "The provided guidelines do not contain an answer to this question."
    lines = []
    for c, _ in chunks[:2]:
        body = c.text.rstrip()
        if body.endswith("."):
            body = body[:-1]
        lines.append(f"{body} [cite:{c.id}].")
    return " ".join(lines)


def generate_live(question: str, chunks: list[tuple[Chunk, float]], settings: Settings | None = None) -> str:
    """Generate with an OpenAI-compatible endpoint (vLLM, Ollama, TGI, hosted). Needs the `openai` package."""
    from openai import OpenAI

    s = settings or Settings()
    client = OpenAI(base_url=s.base_url, api_key=s.api_key or "not-needed")
    ctx = _context([c for c, _ in chunks])
    resp = client.chat.completions.create(
        model=s.model,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {question}"},
        ],
        temperature=0.1,
    )
    return resp.choices[0].message.content or ""


def answer(question: str, chunks: list[tuple[Chunk, float]], settings: Settings | None = None) -> str:
    s = settings or Settings()
    return generate_offline(question, chunks) if s.offline else generate_live(question, chunks, s)
