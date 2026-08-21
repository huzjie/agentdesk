"""agentdesk CLI — `agentdesk <command>`."""
from __future__ import annotations

import argparse
import json
import sys

from .._version import __version__
from ..platform import Platform
from ..skills.catalog import load_catalog
from ..schema import Action


def _json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, default=str)


def cmd_version(args, p: Platform):
    print(f"agentdesk {__version__}")


def cmd_doctor(args, p: Platform):
    report = {
        "version": __version__,
        "provider": p.provider.name,
        "model": p.provider.model,
        "workspace": p.workspace.root,
        "db": p.store.path,
        "sandbox": p.sandbox.mode,
        "computer_mode": p.computer.mode,
        "audit_enabled": p.audit.enabled,
        "employees": len(p.employees.list()),
        "skills": len(p.skills.list()),
        "courses": len(p.catalog.list()),
        "tools": len(p.tools.list()),
    }
    print(_json(report))


def cmd_employee(args, p: Platform):
    if args.sub == "list":
        for e in p.employees.list(status=args.status):
            print(f"{e.id}  {e.name:<20} {e.status:<12} {e.provider}/{e.model}")
    elif args.sub == "create":
        e = p.employees.create(name=args.name, role=args.role, provider=args.provider, model=args.model)
        print(_json(e.to_dict()))
    elif args.sub == "transition":
        e = p.employees.transition(args.id, args.action)
        print(_json(e.to_dict()))
    elif args.sub == "onboard":
        print(_json(p.onboarding.onboard(args.id)))


def cmd_skill(args, p: Platform):
    if args.sub == "list":
        for s in p.skills.list():
            print(f"{s.id}  {s.name}@{s.version:<8} [{s.category}] {s.description}")
    elif args.sub == "load":
        print(f"registered {load_catalog(p.skills)} builtin skills")


def cmd_computer(args, p: Platform):
    if args.sub == "screen":
        print(_json(p.computer.screen.capture(save=True).to_dict()))
    elif args.sub == "run":
        actions = json.loads(args.actions)
        acts = [Action(type=a["type"], params=a.get("params", {})) for a in actions]
        print(_json(p.computer.run_script(acts)))


def cmd_files(args, p: Platform):
    if args.sub == "list":
        print(_json(p.workspace.list()))


def cmd_academy(args, p: Platform):
    if args.sub == "courses":
        for c in p.catalog.list():
            print(f"{c.id:<22} {c.title} [{c.level}]")
    elif args.sub == "assess":
        r = p.assessor.assess(args.employee_id, args.course_id)
        print(_json(r.to_dict()))


def cmd_task(args, p: Platform):
    print(_json(p.run_task(args.task, employee_id=args.employee_id)))


def cmd_serve(args, p: Platform):
    from ..api.app import create_app
    import uvicorn
    app = create_app()
    uvicorn.run(app, host=args.host, port=args.port)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="agentdesk", description="Digital workforce operations")
    parser.add_argument("--config", default=None, help="path to config.json")
    sub = parser.add_subparsers(dest="command")

    p_version = sub.add_parser("version")
    p_version.set_defaults(func=cmd_version)

    p_doctor = sub.add_parser("doctor")
    p_doctor.set_defaults(func=cmd_doctor)

    p_emp = sub.add_parser("employee")
    p_emp.add_argument("sub", choices=["list", "create", "transition", "onboard"])
    p_emp.add_argument("--name")
    p_emp.add_argument("--role", default="generalist")
    p_emp.add_argument("--provider", default="mock")
    p_emp.add_argument("--model", default="mock")
    p_emp.add_argument("--id")
    p_emp.add_argument("--action")
    p_emp.add_argument("--status")
    p_emp.set_defaults(func=cmd_employee)

    p_skill = sub.add_parser("skill")
    p_skill.add_argument("sub", choices=["list", "load"])
    p_skill.set_defaults(func=cmd_skill)

    p_comp = sub.add_parser("computer")
    p_comp.add_argument("sub", choices=["screen", "run"])
    p_comp.add_argument("--actions", default="[]")
    p_comp.set_defaults(func=cmd_computer)

    p_files = sub.add_parser("files")
    p_files.add_argument("sub", choices=["list"])
    p_files.set_defaults(func=cmd_files)

    p_acad = sub.add_parser("academy")
    p_acad.add_argument("sub", choices=["courses", "assess"])
    p_acad.add_argument("--employee-id")
    p_acad.add_argument("--course-id")
    p_acad.set_defaults(func=cmd_academy)

    p_task = sub.add_parser("task")
    p_task.add_argument("task")
    p_task.add_argument("--employee-id", default="")
    p_task.set_defaults(func=cmd_task)

    p_serve = sub.add_parser("serve")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8500)
    p_serve.set_defaults(func=cmd_serve)

    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 1

    if args.config:
        from ..config import load_config as _lc
        p = Platform(_lc(args.config))
    else:
        p = Platform()

    args.func(args, p)
    p.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
