"""Local Ollama provider (OpenAI-compatible local endpoint)."""
from .openai import OpenAIProvider


class OllamaProvider(OpenAIProvider):
    name = "ollama"
    default_model = "llama3.2"

    def __init__(self, base_url: str = "http://localhost:11434/v1", api_key: str = "",
                 model: str = "", timeout: int = 120):
        super().__init__(base_url=base_url, api_key="", model=model, timeout=timeout)
