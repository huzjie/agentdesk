"""OpenAI-compatible provider (also base for DeepSeek/Qwen/Kimi/GLM/Gemini)."""
from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    name = "openai"
    default_model = "gpt-4o-mini"

    def __init__(self, base_url: str = "https://api.openai.com/v1", api_key: str = "",
                 model: str = "", timeout: int = 60):
        super().__init__(base_url=base_url, api_key=api_key, model=model, timeout=timeout)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.2),
        }
        data = self._post_json(f"{self.base_url}/chat/completions", payload)
        choice = (data.get("choices") or [{}])[0]
        return {"content": choice.get("message", {}).get("content", ""), "raw": data}
