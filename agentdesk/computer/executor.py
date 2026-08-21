"""Computer Use action executor — the heart of GUI/desktop automation.

Translates a declarative `Action` into concrete calls on Screen/MouseKeyboard/
Browser, enforces a step budget, and returns an audit-friendly trace.
"""
from __future__ import annotations

from typing import List, Optional

from ..errors import ComputerError, ForbiddenError, ValidationError
from ..schema import Action, ScreenState
from .screen import Screen
from .input import MouseKeyboard
from .browser import Browser

ACTION_TYPES = {
    "screenshot", "click", "double_click", "move", "type_text", "press",
    "scroll", "browser_navigate", "browser_click", "wait",
}


class ComputerExecutor:
    def __init__(self, mode: str = "mock", screenshot_dir: str = "~/.agentdesk/screenshots",
                 max_steps: int = 20, require_approval=None):
        self.mode = mode
        self.screen = Screen(mode=mode, screenshot_dir=screenshot_dir)
        self.input = MouseKeyboard(mode=mode)
        self.browser = Browser(mode=mode)
        self.max_steps = max_steps
        self.require_approval = set(require_approval or [])
        self.trace: List[dict] = []

    def execute(self, action: Action, step: int = 0) -> dict:
        if step >= self.max_steps:
            raise ComputerError(f"step budget exceeded ({self.max_steps})")
        atype = action.type
        if atype not in ACTION_TYPES:
            raise ValidationError(f"unknown action type: {atype}")
        if atype in self.require_approval and action.reason != "approved":
            raise ForbiddenError(f"action '{atype}' requires explicit approval")

        p = action.params
        result = {}
        if atype == "screenshot":
            result = self.screen.capture(save=p.get("save", False)).to_dict()
        elif atype == "click":
            result = self.input.click(int(p["x"]), int(p["y"]), p.get("button", "left"))
        elif atype == "double_click":
            result = self.input.double_click(int(p["x"]), int(p["y"]))
        elif atype == "move":
            result = self.input.move(int(p["x"]), int(p["y"]))
        elif atype == "type_text":
            result = self.input.type_text(p["text"], float(p.get("interval", 0)))
        elif atype == "press":
            result = self.input.press(*p.get("keys", []))
        elif atype == "scroll":
            result = self.input.scroll(int(p.get("clicks", 3)))
        elif atype == "browser_navigate":
            result = self.browser.navigate(p["url"])
        elif atype == "browser_click":
            result = self.browser.click_link(p["url"], p["link_text"])
        elif atype == "wait":
            import time
            time.sleep(min(float(p.get("seconds", 1)), 5))
            result = {"waited": p.get("seconds", 1)}

        self.trace.append({"step": step, "action": action.to_dict(), "result": result})
        return result

    def run_script(self, actions: List[Action]) -> List[dict]:
        out = []
        for i, action in enumerate(actions):
            out.append(self.execute(action, step=i))
        return out
