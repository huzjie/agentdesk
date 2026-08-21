"""Platform — wire all subsystems into a single application object."""
from __future__ import annotations

from typing import Any, Dict, Optional

from .academy import Assessor, Certification, CourseCatalog, FluencyFramework
from .agents import AgentLoop, builtin_tools
from .config import get, load_config
from .computer import ComputerExecutor
from .files import ArtifactManager, Delivery, Workspace
from .observability import Metrics, TraceContext
from .providers import create_provider
from .security import AuditLog, PermissionGate, PolicyEngine, Sandbox, DEFAULT_RULES
from .skills import SkillRegistry
from .storage import SqliteStore
from .workforce import EmployeeRegistry, OnboardingManager


class Platform:
    """The single entry point that wires configuration and all subsystems."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or load_config()
        cfg = self.config

        # persistence + workspace
        self.store = SqliteStore(get(cfg, "agentdesk.db_path", "~/.agentdesk/agentdesk.db"))
        self.workspace = Workspace(get(cfg, "agentdesk.workspace_root", "~/.agentdesk/workspace"))

        # workforce
        self.employees = EmployeeRegistry(self.store)
        self.skills = SkillRegistry(self.store)
        self.onboarding = OnboardingManager(self.employees, self.skills)

        # files + delivery
        self.artifacts = ArtifactManager(self.workspace, self.store)
        self.delivery = Delivery(self.workspace)

        # academy
        self.catalog = CourseCatalog()
        self.framework = FluencyFramework(
            name=get(cfg, "academy.framework", "4d-fluency"),
            pass_threshold=float(get(cfg, "academy.pass_threshold", 0.7)),
        )
        self.assessor = Assessor(self.catalog, self.framework)
        self.certification = Certification(self.workspace)

        # security
        self.sandbox = Sandbox(
            mode=get(cfg, "security.sandbox", "subprocess"),
            deny_network=bool(get(cfg, "security.deny_network", False)),
        )
        self.permission = PermissionGate(PolicyEngine(list(DEFAULT_RULES)))
        self.audit = AuditLog(enabled=bool(get(cfg, "security.audit_enabled", True)))

        # computer use
        self.computer = ComputerExecutor(
            mode=get(cfg, "computer.mode", "mock"),
            screenshot_dir=get(cfg, "computer.screenshot_dir", "~/.agentdesk/screenshots"),
            max_steps=int(get(cfg, "computer.max_steps", 20)),
            require_approval=get(cfg, "security.require_approval", []),
        )

        # provider + agent loop
        self.metrics = Metrics()
        self.provider = self._build_provider()
        self.tools = builtin_tools(self.workspace)
        self.loop = AgentLoop(self.provider, self.tools)

    def _build_provider(self):
        prov = get(self.config, "providers.default", "mock")
        prov_cfg = get(self.config, f"providers.{prov}", {}) or {}
        return create_provider(prov, prov_cfg)

    def run_task(self, task: str, employee_id: str = "") -> Dict[str, Any]:
        self.audit.record(actor=employee_id or "system", action="task:run",
                          resource="agent_loop", detail=task)
        self.metrics.inc("agentdesk_tasks_total")
        trace = TraceContext()
        result = self.loop.run(task, employee_id=employee_id, trace=trace)
        result["traceparent"] = trace.to_traceparent()
        return result

    def close(self):
        self.store.close()
