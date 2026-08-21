"""End-to-end quickstart: create employee, load skills, onboard, run task."""
from agentdesk.platform import Platform
from agentdesk.skills.catalog import load_catalog


def main():
    p = Platform()
    load_catalog(p.skills)

    emp = p.employees.create("Alice", role="analyst")
    print("created:", emp.id, emp.name)

    result = p.onboarding.onboard(emp.id)
    print("onboarded:", result)

    task = p.run_task("write a file", employee_id=emp.id)
    print("task:", task["answer"])
    print("workspace files:", p.workspace.list())

    p.close()


if __name__ == "__main__":
    main()
