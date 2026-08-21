"""Employee lifecycle demo."""
from agentdesk.platform import Platform
from agentdesk.skills.catalog import load_catalog


def main():
    p = Platform()
    load_catalog(p.skills)

    emp = p.employees.create("Bob", role="researcher")
    print("state:", emp.status)

    p.employees.transition(emp.id, "onboard")
    print("state:", p.employees.get(emp.id).status)

    p.employees.transition(emp.id, "complete")
    print("state:", p.employees.get(emp.id).status)

    p.employees.transition(emp.id, "pause")
    print("state:", p.employees.get(emp.id).status)

    p.close()


if __name__ == "__main__":
    main()
