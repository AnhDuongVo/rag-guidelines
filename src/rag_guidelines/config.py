"""Settings for the (optional) live generator. The default is offline extractive generation, no key needed."""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))


@dataclass
class Settings:
    # Neutral, OpenAI-compatible endpoint: point at vLLM, Ollama, TGI, or any hosted API.
    base_url: str = field(default_factory=lambda: os.getenv("RAG_BASE_URL", "http://localhost:8000/v1"))
    api_key: str | None = field(default_factory=lambda: os.getenv("RAG_API_KEY"))
    model: str = field(default_factory=lambda: os.getenv("RAG_MODEL", "local-model"))
    offline: bool = field(default_factory=lambda: os.getenv("RAG_OFFLINE", "1").strip().lower() in {"1", "true", "yes", "on"})
