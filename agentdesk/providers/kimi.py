"""Moonshot Kimi provider (OpenAI-compatible)."""
from .openai import OpenAIProvider


class KimiProvider(OpenAIProvider):
    name = "kimi"
    default_model = "moonshot-v1-8k"

    def __init__(self, base_url: str = "https://api.moonshot.cn/v1", api_key: str = "",
                 model: str = "", timeout: int = 60):
        super().__init__(base_url=base_url, api_key=api_key, model=model, timeout=timeout)
