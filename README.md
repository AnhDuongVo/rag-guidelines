# rag-guidelines

## What this project demonstrates

Demonstrates small-corpus retrieval with citation, lexical, polarity and numerical screening.

## CLI example

![CLI input and output](docs/rag-guidelines.png)

[Portfolio examples](https://anhduongvo.github.io/projects/agentic-tooling/). Clinical recordings use the separate simplified interactive demo.

## Try it offline

Python 3.11–3.13. In a fresh virtual environment, from this repository:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
rag ask "What is the HbA1c target?"
pytest -q
```

## Run with NVIDIA or another configured backend

Install `.[live]`; set `RAG_BASE_URL`, `RAG_API_KEY` when needed, `RAG_MODEL`, and use `rag ask --live`. Select a model served by your endpoint. Live compatibility has not been tested here.

Model IDs in `.env.example` and NAT configs are examples, not a current availability guarantee. Check your endpoint before running; the validation below does not include live model execution.

## What is verified

Every cited ID exists, selected numerical values occur in sources, and lexical/polarity screens pass. These signals are not clinical entailment. The synthetic corpus is educational.

| Validation layer | Status |
|---|---|
| Unit/regression tests | Executed locally on Python 3.12; see `docs/validation.md` |
| Mocked/simulated integrations | Executed locally; scope documented in tests |
| Live hosted endpoints | Not executed; access and appropriate inputs required |
| Self-hosted GPU endpoints | Not executed |
| Domain-specific validation | Not completed; synthetic examples only |

See [validation details](docs/validation.md). The architecture and detailed workflows follow.

## Architecture and detailed workflows

**Retrieval-augmented generation over clinical guidelines and drug labels, with lightweight screening against cited sources.** It retrieves the relevant passages, answers only from them, and then checks each sentence of the answer against the chunk it cites, flagging anything unsupported or any number that is not in the source. Built on a neutral, OpenAI-compatible stack (vLLM, Ollama, TGI, or any hosted API), with an offline mode that needs no key.

## Demo

An HbA1c question is answered extractively from the synthetic corpus, with retrieved sources, scores and lexical/numerical screening. No live clinical LLM is evaluated. The command/output examples are on [anhduongvo.github.io](https://anhduongvo.github.io/projects/agentic-tooling/).

## Why

A model can retrieve the right guideline passage and still state a dose the passage does not mention. This project adds a verification step after generation: every sentence is checked against the chunk it cites (content overlap and exact numbers), and unsupported sentences are flagged.

## How it works

1. **Retrieve** the top passages with a small, dependency-free TF-IDF retriever.
2. **Generate** an answer that cites each passage as `[cite:<id>]`. Offline mode is extractive from the supplied corpus; live mode calls any OpenAI-compatible endpoint with a strict "answer only from context" prompt.
3. **Verify** every sentence against its cited chunk: enough content words must overlap, and every number must appear in the source. Unsupported sentences are flagged.

## Quickstart

```bash
pip install -e ".[dev]"

rag ask "what is the maximum metformin dose?"     # offline, no key
rag corpus                                          # list the (synthetic) sources
```

Example: the answer "The maximum recommended daily dose of metformin is 2550 mg ... [cite:met-1]" is checked against chunk `met-1`; a fabricated "9999 mg [cite:met-1]" is flagged because the number is not in the source.

## Live generation (neutral stack)

```bash
RAG_OFFLINE=0
RAG_BASE_URL=http://localhost:8000/v1   # vLLM / Ollama / TGI / hosted, your choice
RAG_API_KEY=...                         # if your endpoint needs one
RAG_MODEL=your-model-name
rag ask "first-line treatment for hypertension?" --live
```

## A note on the corpus

The bundled corpus is **synthetic**: short guideline- and label-style snippets written for the demo, not copied from any real guideline or label. Replace `corpus.py` (or load from public sources) to use it for real.

## Development

```bash
ruff check .
pytest
```

## License

Apache-2.0.
