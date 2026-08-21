"""DeepSeek provider (OpenAI-compatible)."""
from .openai import OpenAIProvider


class DeepSeekProvider(OpenAIProvider):
    name = "deepseek"
    default_model = "deepseek-chat"

    def __init__(self, base_url: str = "https://api.deepseek.com/v1", api_key: str = "",
                 model: str = "", timeout: int = 60):
        super().__init__(base_url=base_url, api_key=api_key, model=model, timeout=timeout)
