from typing import Protocol, Any


class AIModel(Protocol):
    """Provide an interface for AI models."""

    def model_name(self) -> str:
        ...

