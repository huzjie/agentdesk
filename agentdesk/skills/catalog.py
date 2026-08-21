"""Built-in skill catalog (starter packs).

These are declarative skill definitions so the platform ships with a useful,
immediately-registerable skill library. Real skill logic is executed through
the agent loop + tools; the catalog provides metadata, parameters and tags.
"""
from __future__ import annotations

from typing import List

from .skill import SkillDef

BUILTIN_SKILLS: List[SkillDef] = [
    SkillDef(
        name="text_summary", version="1.0.0", category="content",
        description="Summarize a long document into concise bullet points.",
        parameters=[
            {"name": "text", "type": "string", "required": True},
            {"name": "max_bullets", "type": "integer", "required": False, "default": 5},
        ],
        tags=["summarize", "content", "nlp"],
    ),
    SkillDef(
        name="email_draft", version="1.0.0", category="office",
        description="Draft a professional email from a short brief.",
        parameters=[
            {"name": "brief", "type": "string", "required": True},
            {"name": "tone", "type": "string", "required": False, "default": "professional"},
        ],
        tags=["email", "office", "writing"],
    ),
    SkillDef(
        name="web_lookup", version="1.0.0", category="research",
        description="Fetch and extract the main content of a web page.",
        parameters=[
            {"name": "url", "type": "string", "required": True},
            {"name": "max_chars", "type": "integer", "required": False, "default": 4000},
        ],
        tags=["web", "research", "scrape"],
    ),
    SkillDef(
        name="file_report", version="1.0.0", category="office",
        description="Generate a structured Markdown report and save it as a deliverable file.",
        parameters=[
            {"name": "title", "type": "string", "required": True},
            {"name": "sections", "type": "array", "required": True},
        ],
        tags=["report", "markdown", "deliverable"],
    ),
    SkillDef(
        name="screen_capture", version="1.0.0", category="computer",
        description="Capture the current screen and describe its visible elements.",
        parameters=[
            {"name": "save", "type": "boolean", "required": False, "default": True},
        ],
        tags=["computer-use", "screenshot", "gui"],
    ),
    SkillDef(
        name="spreadsheet_fill", version="1.0.0", category="office",
        description="Fill a CSV/table template from structured rows.",
        parameters=[
            {"name": "rows", "type": "array", "required": True},
            {"name": "filename", "type": "string", "required": True},
        ],
        tags=["csv", "office", "data"],
    ),
]


def load_catalog(registry) -> int:
    """Register all built-in skills into a registry. Returns count registered."""
    count = 0
    for skill_def in BUILTIN_SKILLS:
        try:
            registry.register(skill_def)
            count += 1
        except Exception:
            pass
    return count
