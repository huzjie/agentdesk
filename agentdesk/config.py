"""Configuration loader for agentdesk.

Supports (in priority order):
  1. Environment variables (AGENTDESK_* with `__` as nested separator).
  2. A JSON config file (config.json) — optional.
  3. Built-in defaults.

JSON is used deliberately (no YAML dependency) to keep the kernel stdlib-only.
"""
from __future__ import annotations

import copy
import json
import os
from typing import Any, Dict, Optional

from .errors import ConfigError

DEFAULTS: Dict[str, Any] = {
    "agentdesk": {
        "name": "AgentDesk",
        "workspace_root": "~/.agentdesk/workspace",
        "db_path": "~/.agentdesk/agentdesk.db",
        "log_level": "INFO",
    },
    "server": {
        "host": "127.0.0.1",
        "port": 8500,
        "api_key": "",
    },
    "computer": {
        "mode": "mock",           # mock | pyautogui | browser
        "screenshot_dir": "~/.agentdesk/screenshots",
        "headless": True,
        "max_steps": 20,
    },
    "security": {
        "sandbox": "subprocess",   # subprocess | docker | none
        "deny_network": False,
        "require_approval": ["shell", "browser_navigate"],
        "audit_enabled": True,
    },
    "academy": {
        "pass_threshold": 0.7,
        "framework": "4d-fluency",
    },
    "providers": {
        "default": "mock",
        "mock": {"base_url": "", "model": "mock", "api_key": ""},
    },
}


def _expand(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))


def _deep_merge(base: Dict, override: Dict) -> Dict:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _parse_env() -> Dict[str, Any]:
    """Parse AGENTDESK_* environment variables into a nested dict."""
    env: Dict[str, Any] = {}
    prefix = "AGENTDESK_"
    for key, val in os.environ.items():
        if not key.startswith(prefix):
            continue
        val = val.strip()
        if val == "":
            continue
        parts = key[len(prefix):].lower().split("__")
        node = env
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        # best-effort scalar typing
        node[parts[-1]] = _coerce(val)
    return env


def _coerce(val: str):
    low = val.lower()
    if low in ("true", "false"):
        return low == "true"
    if low in ("null", "none"):
        return None
    try:
        return int(val)
    except ValueError:
        pass
    try:
        return float(val)
    except ValueError:
        pass
    return val


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """Load config, merging defaults <- file <- environment."""
    config = copy.deepcopy(DEFAULTS)

    candidates = []
    if path:
        candidates.append(path)
    candidates.append(os.environ.get("AGENTDESK_CONFIG", ""))
    candidates.append("config.json")
    candidates.append("agentdesk.json")

    loaded = None
    for c in candidates:
        if not c:
            continue
        if os.path.isfile(_expand(c)):
            try:
                with open(_expand(c), "r", encoding="utf-8") as f:
                    loaded = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                raise ConfigError(f"failed to parse config file {c}: {e}")
            break

    if loaded:
        config = _deep_merge(config, loaded)
    config = _deep_merge(config, _parse_env())

    # expand paths
    config["agentdesk"]["workspace_root"] = _expand(config["agentdesk"]["workspace_root"])
    config["agentdesk"]["db_path"] = _expand(config["agentdesk"]["db_path"])
    config["computer"]["screenshot_dir"] = _expand(config["computer"]["screenshot_dir"])
    return config


def get(cfg: Dict[str, Any], dotted: str, default: Any = None) -> Any:
    """Dotted-path getter, e.g. get(cfg, "server.port")."""
    node: Any = cfg
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node
