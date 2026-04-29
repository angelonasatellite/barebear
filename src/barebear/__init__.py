from __future__ import annotations

from barebear.bear import Bear
from barebear.budget import Budget
from barebear.checkpoint import Checkpoint, CheckpointManager
from barebear.exceptions import (
    BudgetExceeded,
    CheckpointRequired,
    PolicyViolation,
    ToolExecutionError,
)
from barebear.models import (
    ModelAdapter,
    ModelResponse,
    OllamaModel,
    OpenAIModel,
    OpenRouterModel,
)
from barebear.policy import Policy
from barebear.reflect import Reflect, Reflection
from barebear.report import Report
from barebear.state import State
from barebear.task import Task
from barebear.tool import Tool, ToolRegistry
from barebear.uncertainty import Uncertainty

__all__ = [
    "Bear",
    "Budget",
    "Checkpoint",
    "CheckpointManager",
    "ModelAdapter",
    "ModelResponse",
    "OllamaModel",
    "OpenAIModel",
    "OpenRouterModel",
    "Policy",
    "Reflect",
    "Reflection",
    "Report",
    "State",
    "Task",
    "Tool",
    "ToolRegistry",
    "Uncertainty",
    "BudgetExceeded",
    "CheckpointRequired",
    "PolicyViolation",
    "ToolExecutionError",
]

__version__ = "0.3.0"
