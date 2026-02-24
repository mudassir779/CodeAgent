"""Shared types for LLM communication."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Message:
    """A single message in the conversation."""
    role: str  # "user", "assistant", "system", "tool"
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str | None = None
    name: str | None = None  # tool name for tool-result messages


@dataclass
class ToolCall:
    """A tool invocation requested by the LLM."""
    id: str
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    """Result of executing a tool."""
    tool_call_id: str
    name: str
    content: str
    is_error: bool = False


@dataclass
class LLMResponse:
    """Parsed response from an LLM provider."""
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    stop_reason: str | None = None

    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0
