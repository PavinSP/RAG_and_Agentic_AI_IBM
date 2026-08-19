# Local Ollama Version

Runnable rewrite of the lab's Flask + LangChain project, swapping IBM watsonx.ai models (Llama, Granite, Mistral) for local Ollama models (`qwen2.5:7b`, `qwen2.5:14b`), so it runs fully offline with no API key. Includes both the JSON-structured-output chain and the full browser chat UI from the lab.

## Files

- `ollama_llm.py` — `OllamaLLM`, a minimal LangChain `LLM` wrapper that calls the local Ollama HTTP API. Stands in for `ChatWatsonx`.
- `config.py` — model parameters and the two local model IDs (equivalent of the lab's `config.py`).
- `model.py` — initializes the models and defines two parallel chains:
  - `qwen_small_response` / `qwen_large_response` — `template | model | json_parser`, returning validated JSON matching the `AIResponse` schema (`summary`, `sentiment`, `category`, `action` — includes the "Enhancing the JSON Structure" exercise fields).
  - `qwen_small_plain_response` / `qwen_large_plain_response` — plain `template | model`, returning conversational text, used by the chat UI (the lab's final `/generate` route expects plain text in a `response` field, not the structured schema).
- `llm_test.py` — sanity check that calls both models directly with a support-style message and prints their structured JSON responses (equivalent of the lab's `llm_test.py`).
- `app.py` — the Flask app. `GET /` serves `templates/index.html`; `POST /generate` takes `{message, model}` and returns `{response, duration}` or `{error}`, matching what `static/script.js` expects.
- `templates/index.html` — the lab's chat UI, with the model `<select>` options changed to `small`/`large` to match the two local Ollama models available here.
- `static/script.js`, `static/styles.css` — fetched as-is from the lab's GitHub Gists (only the hardcoded default model value in `script.js` was changed, from `llama3` to `small`, to match this project's model options).

## Prerequisites

- [Ollama](https://ollama.com) running locally (`ollama serve`, usually automatic after install).
- Models pulled: `ollama pull qwen2.5:7b` and `ollama pull qwen2.5:14b` (any other pulled chat model works too — just update `config.py`).
- The repo's root `.venv` activated, with `Flask`, `langchain-core`, and `pydantic` installed.

## Running

```bash
source "/Users/pavinsp/Downloads/IBM RAG and Agentic AI/.venv/bin/activate"
cd "local_ollama_app"
python3 llm_test.py   # sanity check — calls both models directly, prints structured JSON
python3 app.py         # starts the Flask server on http://127.0.0.1:5000
```

Then open `http://127.0.0.1:5000` in a browser for the chat UI, or call the API directly:

```bash
curl -X POST http://127.0.0.1:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of Canada?", "model": "small"}'
```

`model` accepts `"small"` (`qwen2.5:7b`) or `"large"` (`qwen2.5:14b`).

Verified end-to-end:
- `llm_test.py` — both models return valid, schema-conforming JSON via the `template | model | json_parser` chain.
- The web app — page loads, `static/script.js` and `static/styles.css` serve correctly, `/generate` returns `{response, duration}` for valid requests and the expected `{error}` for a missing message/model or an invalid model choice.
