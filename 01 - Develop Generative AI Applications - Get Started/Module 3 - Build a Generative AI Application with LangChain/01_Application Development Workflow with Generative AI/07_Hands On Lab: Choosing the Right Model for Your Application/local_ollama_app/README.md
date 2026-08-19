# Local Ollama Version

Runnable rewrite of the lab's Flask + LangChain project, swapping IBM watsonx.ai models (Llama, Granite, Mistral) for local Ollama models (`qwen2.5:7b`, `qwen2.5:14b`), so it runs fully offline with no API key.

## Files

- `ollama_llm.py` — `OllamaLLM`, a minimal LangChain `LLM` wrapper that calls the local Ollama HTTP API. Stands in for `ChatWatsonx`.
- `config.py` — model parameters and the two local model IDs (equivalent of the lab's `config.py`).
- `model.py` — initializes the models, defines the Qwen ChatML prompt template, and exposes `qwen_small_response` / `qwen_large_response` (equivalent of the lab's `model.py`).
- `llm_test.py` — sanity check that calls both models directly and prints their responses (equivalent of the lab's `llm_test.py`).
- `app.py` — the Flask app with a `/generate` endpoint that calls a chosen model and parses its output as JSON via LangChain's `JsonOutputParser`.

## Prerequisites

- [Ollama](https://ollama.com) running locally (`ollama serve`, usually automatic after install).
- Models pulled: `ollama pull qwen2.5:7b` and `ollama pull qwen2.5:14b` (any other pulled chat model works too — just update `config.py`).
- The repo's root `.venv` activated, with `Flask` and `langchain-core` installed.

## Running

```bash
source "/Users/pavinsp/Downloads/IBM RAG and Agentic AI/.venv/bin/activate"
cd "local_ollama_app"
python3 llm_test.py   # sanity check — calls both models directly
python3 app.py         # starts the Flask server on http://127.0.0.1:5000
```

Then, in another terminal:

```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the capital of France? Respond as JSON with keys country and capital.", "model": "small"}'
```

`model` accepts `"small"` (`qwen2.5:7b`) or `"large"` (`qwen2.5:14b`).

Verified end-to-end: both models return valid JSON via `JsonOutputParser`, and the endpoint's error paths (missing prompt, unknown model, non-JSON model output) all return the expected error responses.
