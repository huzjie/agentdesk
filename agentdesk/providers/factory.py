"""Provider factory — map a name to a concrete provider class."""
from __future__ import annotations

from typing import Any, Dict

from ..errors import ConfigError
from .anthropic import AnthropicProvider
from .deepseek import DeepSeekProvider
from .gemini import GeminiProvider
from .glm import GLMProvider
from .kimi import KimiProvider
from .mock import MockProvider
from .ollama import OllamaProvider
from .openai import OpenAIProvider
from .qwen import QwenProvider

_PROVIDERS = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "deepseek": DeepSeekProvider,
    "qwen": QwenProvider,
    "kimi": KimiProvider,
    "glm": GLMProvider,
    "gemini": GeminiProvider,
    "ollama": OllamaProvider,
    "mock": MockProvider,
}


def create_provider(name: str, cfg: Dict[str, Any] = None):
    cfg = cfg or {}
    cls = _PROVIDERS.get(name)
    if cls is None:
        raise ConfigError(f"unknown provider: {name}")
    kwargs = {
        "base_url": cfg.get("base_url", ""),
        "api_key": cfg.get("api_key", ""),
        "model": cfg.get("model", ""),
    }
    return cls(**kwargs)


def provider_names():
    return sorted(_PROVIDERS.keys())
