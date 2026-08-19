import requests
from typing import Optional, List
from langchain_core.language_models.llms import LLM


class OllamaLLM(LLM):
    """Minimal LangChain-compatible wrapper around a local Ollama model,
    used in place of ChatWatsonx so this project runs without cloud credentials."""
    model: str = "qwen2.5:7b"
    temperature: float = 0.0
    max_tokens: int = 256

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": self.temperature, "num_predict": self.max_tokens},
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["response"]
