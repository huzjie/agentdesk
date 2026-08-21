"""Exception hierarchy for agentdesk."""


class AgentDeskError(Exception):
    """Base class for all agentdesk errors."""

    code = "AGENTDESK_ERROR"

    def __init__(self, message="", code=None):
        super().__init__(message)
        self.message = message
        if code:
            self.code = code

    def to_dict(self):
        return {"code": self.code, "message": self.message}


class ConfigError(AgentDeskError):
    code = "CONFIG_ERROR"


class NotFoundError(AgentDeskError):
    code = "NOT_FOUND"


class ConflictError(AgentDeskError):
    code = "CONFLICT"


class ValidationError(AgentDeskError):
    code = "VALIDATION_ERROR"


class AuthError(AgentDeskError):
    code = "AUTH_ERROR"


class ForbiddenError(AgentDeskError):
    code = "FORBIDDEN"


class SandboxError(AgentDeskError):
    code = "SANDBOX_ERROR"


class SkillError(AgentDeskError):
    code = "SKILL_ERROR"


class ComputerError(AgentDeskError):
    code = "COMPUTER_ERROR"


class ProviderError(AgentDeskError):
    code = "PROVIDER_ERROR"


class RateLimitError(AgentDeskError):
    code = "RATE_LIMITED"
