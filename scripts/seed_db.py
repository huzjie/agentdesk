"""Seed the database with starter skills and a demo employee."""
from agentdesk.platform import Platform
from agentdesk.skills.catalog import load_catalog


def main():
    p = Platform()
    n = load_catalog(p.skills)
    print("registered skills:", n)
    emp = p.employees.create("Demo Employee", role="generalist")
    print("created employee:", emp.id)
    p.close()


if __name__ == "__main__":
    main()
