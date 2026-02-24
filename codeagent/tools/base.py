"""Abstract base class for tools."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Every tool must define its name, description, schema, and execute method."""

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        ...

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """JSON Schema for the tool parameters."""
        ...

    @abstractmethod
    def execute(self, **kwargs: Any) -> str:
        """Run the tool and return a string result."""
        ...

    def to_schema(self) -> dict[str, Any]:
        """Return the tool definition for the LLM."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }
