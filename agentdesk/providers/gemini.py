"""Google Gemini provider (OpenAI-compatible endpoint)."""
from .openai import OpenAIProvider


class GeminiProvider(OpenAIProvider):
    name = "gemini"
    default_model = "gemini-2.5-flash"

    def __init__(self, base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai",
                 api_key: str = "", model: str = "", timeout: int = 60):
        super().__init__(base_url=base_url, api_key=api_key, model=model, timeout=timeout)
