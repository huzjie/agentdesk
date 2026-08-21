"""Provider base class and shared HTTP helpers."""
from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict, List, Optional

from ..errors import ProviderError


class BaseProvider:
    name = "base"
    default_model = ""

    def __init__(self, base_url: str = "", api_key: str = "", model: str = "",
                 timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model or self.default_model
        self.timeout = timeout

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

    def _post_json(self, url: str, payload: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        hdrs = {"Content-Type": "application/json"}
        if self.api_key:
            hdrs["Authorization"] = f"Bearer {self.api_key}"
        if headers:
            hdrs.update(headers)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST", headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {}
        except Exception as e:
            raise ProviderError(f"{self.name} request failed: {e}")
