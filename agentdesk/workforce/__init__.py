"""Digital workforce: employees, registry, onboarding."""

from .employee import employee_state_machine, available_actions
from .registry import EmployeeRegistry
from .onboarding import OnboardingManager

__all__ = ["employee_state_machine", "available_actions", "EmployeeRegistry", "OnboardingManager"]
