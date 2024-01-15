from typing import Protocol, List


class AIModel(Protocol):
    """Provide an interface for AI models."""

    def model_name(self) -> str:
        """Get the official model's name."""
        ...
