"""FastAPI control plane (optional dependency)."""


def create_app(config=None):
    from .app import create_app as _create
    return _create(config)
