"""Computer Use action demo (mock mode)."""
from agentdesk.computer import ComputerExecutor
from agentdesk.schema import Action


def main():
    ex = ComputerExecutor(mode="mock")
    results = ex.run_script([
        Action(type="screenshot"),
        Action(type="click", params={"x": 200, "y": 100}),
        Action(type="type_text", params={"text": "hello agentdesk"}),
        Action(type="browser_navigate", params={"url": "https://example.com"}),
    ])
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
