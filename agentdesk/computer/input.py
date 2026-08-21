"""Mouse and keyboard input abstraction (mockable)."""
from __future__ import annotations

from typing import Dict, List

from ..errors import ComputerError


class MouseKeyboard:
    def __init__(self, mode: str = "mock"):
        self.mode = mode
        self.log: List[Dict] = []

    def _record(self, action: str, **kwargs) -> dict:
        entry = {"action": action, **kwargs}
        self.log.append(entry)
        return entry

    def click(self, x: int, y: int, button: str = "left") -> dict:
        if self.mode == "pyautogui":
            try:
                import pyautogui
                pyautogui.click(x, y, button=button)
            except Exception as e:
                raise ComputerError(f"click failed: {e}")
        return self._record("click", x=x, y=y, button=button)

    def double_click(self, x: int, y: int) -> dict:
        if self.mode == "pyautogui":
            try:
                import pyautogui
                pyautogui.doubleClick(x, y)
            except Exception as e:
                raise ComputerError(f"double_click failed: {e}")
        return self._record("double_click", x=x, y=y)

    def move(self, x: int, y: int) -> dict:
        if self.mode == "pyautogui":
            try:
                import pyautogui
                pyautogui.moveTo(x, y)
            except Exception as e:
                raise ComputerError(f"move failed: {e}")
        return self._record("move", x=x, y=y)

    def type_text(self, text: str, interval: float = 0.0) -> dict:
        if self.mode == "pyautogui":
            try:
                import pyautogui
                pyautogui.write(text, interval=interval)
            except Exception as e:
                raise ComputerError(f"type_text failed: {e}")
        return self._record("type_text", text=text, interval=interval)

    def press(self, *keys: str) -> dict:
        if self.mode == "pyautogui":
            try:
                import pyautogui
                pyautogui.hotkey(*keys)
            except Exception as e:
                raise ComputerError(f"press failed: {e}")
        return self._record("press", keys=list(keys))

    def scroll(self, clicks: int) -> dict:
        if self.mode == "pyautogui":
            try:
                import pyautogui
                pyautogui.scroll(clicks)
            except Exception as e:
                raise ComputerError(f"scroll failed: {e}")
        return self._record("scroll", clicks=clicks)
