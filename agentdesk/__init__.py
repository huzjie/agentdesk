"""
agentdesk - Enterprise Digital Workforce Operations Platform.

Turn LLMs into managed "digital employees": onboard them, give them reusable
skills, let them operate computers (Computer Use), produce deliverable files
(Files API), and train/assess them through an academy (4D AI Fluency).

The core kernel is pure Python standard library (zero third-party runtime
dependency). A FastAPI control plane, CLI, Python/TypeScript SDKs and a React
console sit on top, but everything can run fully offline in `mock` mode.
"""

from ._version import __version__

__all__ = ["__version__"]
