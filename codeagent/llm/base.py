"""Abstract base class for LLM providers."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from .types import LLMResponse, Message


class BaseLLMProvider(ABC):
    """Interface that all LLM providers must implement."""

    @abstractmethod
    def chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        system: str = "",
    ) -> LLMResponse:
        """Send messages and return a complete response."""
        ...

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        system: str = "",
    ) -> AsyncIterator[str]:
        """Stream text chunks from the LLM. Yields text deltas."""
        ...
        # Make it a valid async generator
        yield ""  # pragma: no cover

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the display name of the current model."""
        ...
