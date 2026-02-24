"""Claude (Anthropic) LLM provider."""

from __future__ import annotations
import json
from typing import Any, AsyncIterator

import anthropic

from ..config import config
from ..constants import CLAUDE_MODEL
from .base import BaseLLMProvider
from .types import LLMResponse, Message, ToolCall


def _messages_to_anthropic(messages: list[Message]) -> list[dict]:
    """Convert internal messages to Anthropic API format."""
    result = []
    for msg in messages:
        if msg.role == "tool":
            result.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": msg.tool_call_id,
                        "content": msg.content,
                        "is_error": False,
                    }
                ],
            })
        elif msg.role == "assistant" and msg.tool_calls:
            content: list[dict] = []
            if msg.content:
                content.append({"type": "text", "text": msg.content})
            for tc in msg.tool_calls:
                content.append({
                    "type": "tool_use",
                    "id": tc.id,
                    "name": tc.name,
                    "input": tc.arguments,
                })
            result.append({"role": "assistant", "content": content})
        elif msg.role in ("user", "assistant"):
            result.append({"role": msg.role, "content": msg.content})
    return result


def _tools_to_anthropic(tools: list[dict[str, Any]]) -> list[dict]:
    """Convert tool schemas to Anthropic format."""
    result = []
    for tool in tools:
        result.append({
            "name": tool["name"],
            "description": tool["description"],
            "input_schema": tool["parameters"],
        })
    return result


class AnthropicProvider(BaseLLMProvider):
    """Claude API provider."""

    def __init__(self, model: str = CLAUDE_MODEL) -> None:
        self.model = model
        self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)

    def chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        system: str = "",
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 8192,
            "messages": _messages_to_anthropic(messages),
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = _tools_to_anthropic(tools)

        response = self.client.messages.create(**kwargs)

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input if isinstance(block.input, dict) else {},
                    )
                )

        return LLMResponse(
            content="\n".join(text_parts),
            tool_calls=tool_calls,
            stop_reason=response.stop_reason,
        )

    async def stream_chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        system: str = "",
    ) -> AsyncIterator[str]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": 8192,
            "messages": _messages_to_anthropic(messages),
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = _tools_to_anthropic(tools)

        with self.client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text

    def get_model_name(self) -> str:
        return f"Claude ({self.model})"
