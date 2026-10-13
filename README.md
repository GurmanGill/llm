$ llm

## Incident extractor

The incident extractor uses Ollama's OpenAI-compatible API. Set
`ollama_local_baseurl` in your `.env` to `http://localhost:11434` or
`http://localhost:11434/v1`; the script adds `/v1` if needed. Set
`ollama_local_api_key` to a nonempty placeholder such as `ollama` for local
Ollama, and ensure the `qwen3.5:4b` model is installed.

Run from this directory:

```sh
.venv/bin/python logs/playground/incident_extractor/main.py
```
