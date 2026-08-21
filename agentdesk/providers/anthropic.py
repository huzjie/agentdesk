"""Anthropic Messages API provider."""
from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    name = "anthropic"
    default_model = "claude-sonnet-4-5"

    def __init__(self, base_url: str = "https://api.anthropic.com/v1", api_key: str = "",
                 model: str = "", timeout: int = 60):
        super().__init__(base_url=base_url, api_key=api_key, model=model, timeout=timeout)

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        system = "\n".join(m["content"] for m in messages if m["role"] == "system")
        turns = [m for m in messages if m["role"] != "system"]
        payload = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "messages": turns,
        }
        if system:
            payload["system"] = system
        data = self._post_json(f"{self.base_url}/messages", payload, headers={
            "x-api-key": self.api_key, "anthropic-version": "2023-06-01",
        })
        content = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
        return {"content": content, "raw": data}
