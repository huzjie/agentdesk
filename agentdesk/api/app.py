"""FastAPI application factory."""
from __future__ import annotations

from fastapi import FastAPI

from .._version import __version__
from .deps import get_platform
from .routers import academy, admin, computer, employees, files, skills, tasks


def create_app(config=None) -> FastAPI:
    app = FastAPI(
        title="AgentDesk",
        description="Enterprise Digital Workforce Operations Platform",
        version=__version__,
    )

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    @app.get("/readyz")
    def readyz():
        p = get_platform()
        return {"status": "ready", "provider": p.provider.name, "model": p.provider.model}

    @app.get("/version")
    def version():
        return {"version": __version__}

    @app.get("/metrics")
    def metrics():
        p = get_platform()
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(p.metrics.render_prometheus())

    app.include_router(employees.router)
    app.include_router(skills.router)
    app.include_router(computer.router)
    app.include_router(files.router)
    app.include_router(academy.router)
    app.include_router(tasks.router)
    app.include_router(admin.router)
    return app


app = create_app()
