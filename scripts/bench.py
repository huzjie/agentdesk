"""Quick benchmark of the agent loop and registry (mock provider)."""
import time

from agentdesk.platform import Platform
from agentdesk.skills.catalog import load_catalog


def main():
    p = Platform()
    load_catalog(p.skills)

    t0 = time.time()
    for _ in range(100):
        p.employees.create("bench")
    t1 = time.time()
    print(f"employee create x100: {t1 - t0:.3f}s")

    t0 = time.time()
    for _ in range(50):
        p.run_task("echo hello")
    t1 = time.time()
    print(f"task run x50: {t1 - t0:.3f}s")

    p.close()


if __name__ == "__main__":
    main()
