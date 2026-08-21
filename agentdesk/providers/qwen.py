"""Alibaba Qwen provider (OpenAI-compatible)."""
from .openai import OpenAIProvider


class QwenProvider(OpenAIProvider):
    name = "qwen"
    default_model = "qwen-plus"

    def __init__(self, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1",
                 api_key: str = "", model: str = "", timeout: int = 60):
        super().__init__(base_url=base_url, api_key=api_key, model=model, timeout=timeout)
