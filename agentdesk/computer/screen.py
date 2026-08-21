"""Screen abstraction: capture, resolution, element registry.

In `mock` mode no real capture happens; we synthesize a virtual desktop so the
platform is fully testable offline. In `pyautogui` mode we delegate to the
optional pyautogui backend if installed.
"""
from __future__ import annotations

import base64
import os
import time
from typing import List, Optional

from ..errors import ComputerError
from ..schema import ScreenState


class Screen:
    def __init__(self, mode: str = "mock", screenshot_dir: str = "~/.agentdesk/screenshots"):
        self.mode = mode
        self.screenshot_dir = os.path.expanduser(screenshot_dir)
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def resolution(self) -> tuple:
        if self.mode == "pyautogui":
            try:
                import pyautogui
                return pyautogui.size()
            except Exception as e:
                raise ComputerError(f"pyautogui unavailable: {e}")
        return (1920, 1080)

    def capture(self, save: bool = False) -> ScreenState:
        w, h = self.resolution()
        if self.mode == "pyautogui":
            try:
                import pyautogui
                img = pyautogui.screenshot()
                path = None
                if save:
                    path = os.path.join(self.screenshot_dir, f"shot_{int(time.time())}.png")
                    img.save(path)
                return ScreenState(width=w, height=h, screenshot=path)
            except Exception as e:
                raise ComputerError(f"capture failed: {e}")
        # mock mode: return a synthetic screen with deterministic elements
        elements = [
            {"type": "window", "label": "AgentDesk Console", "bbox": [0, 0, 1280, 800]},
            {"type": "button", "label": "New Task", "bbox": [1150, 40, 1240, 80]},
            {"type": "input", "label": "prompt", "bbox": [400, 720, 1200, 760]},
            {"type": "text", "label": "ready", "bbox": [40, 120, 400, 160]},
        ]
        return ScreenState(width=w, height=h, screenshot="mock", elements=elements)
