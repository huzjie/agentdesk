"""Browser operation abstraction (navigate, extract, click).

A real browser can be attached via optional Selenium/Playwright drivers; the
default `urllib`-based extractor works fully offline for static pages. The
mock driver lets tests run without any network.
"""
from __future__ import annotations

import re
import urllib.request
from typing import Optional

from ..errors import ComputerError

_TAG_RE = re.compile(r"<[^>]+>")


class Browser:
    def __init__(self, mode: str = "mock", timeout: int = 15, user_agent: str = "agentdesk/1.0"):
        self.mode = mode
        self.timeout = timeout
        self.user_agent = user_agent
        self.history = []

    def navigate(self, url: str) -> dict:
        self.history.append(("navigate", url))
        if self.mode == "mock":
            return {"url": url, "status": 200, "title": "mock page", "len": 0}
        return self.fetch(url)

    def fetch(self, url: str, max_chars: int = 4000) -> dict:
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8", "replace")
                title = ""
                m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.I | re.S)
                if m:
                    title = _TAG_RE.sub("", m.group(1)).strip()
                text = _TAG_RE.sub(" ", raw)
                text = re.sub(r"\s+", " ", text).strip()
                return {
                    "url": url, "status": resp.status, "title": title,
                    "text": text[:max_chars], "len": len(text),
                }
        except Exception as e:
            raise ComputerError(f"navigate failed: {e}")

    def click_link(self, url: str, link_text: str) -> dict:
        self.history.append(("click", url, link_text))
        if self.mode == "mock":
            return {"clicked": link_text, "url": url, "ok": True}
        page = self.fetch(url, max_chars=100000)
        m = re.search(r'href=["\']([^"\']+)["\'][^>]*>' + re.escape(link_text) + r"<", page["text"], re.I)
        if not m:
            raise ComputerError(f"link not found: {link_text}")
        return self.navigate(m.group(1))
