"""Zhipu GLM provider (OpenAI-compatible)."""
from .openai import OpenAIProvider


class GLMProvider(OpenAIProvider):
    name = "glm"
    default_model = "glm-4-plus"

    def __init__(self, base_url: str = "https://open.bigmodel.cn/api/paas/v4", api_key: str = "",
                 model: str = "", timeout: int = 60):
        super().__init__(base_url=base_url, api_key=api_key, model=model, timeout=timeout)
