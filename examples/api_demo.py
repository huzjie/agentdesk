"""FastAPI control plane demo (requires `pip install -e ".[api]"`)."""
from agentdesk.api.app import create_app
from fastapi.testclient import TestClient


def main():
    app = create_app()
    client = TestClient(app)
    print("healthz:", client.get("/healthz").json())
    print("version:", client.get("/version").json())
    emp = client.post("/employees", json={"name": "Alice"}).json()
    print("employee:", emp)
    courses = client.get("/academy/courses").json()
    print("courses:", [c["id"] for c in courses])


if __name__ == "__main__":
    main()
