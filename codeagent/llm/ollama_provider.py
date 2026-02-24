"""Ollama local LLM provider — free, no API key needed."""

from __future__ import annotations
import json
from typing import Any, AsyncIterator

import openai

from .base import BaseLLMProvider
from .types import LLMResponse, Message, ToolCall


def _messages_to_ollama(messages: list[Message], system: str = "") -> list[dict]:
    """Convert internal messages to OpenAI-compatible format for Ollama."""
    result: list[dict] = []
    if system:
        result.append({"role": "system", "content": system})

    for msg in messages:
        if msg.role == "tool":
            result.append({
                "role": "tool",
                "tool_call_id": msg.tool_call_id,
                "content": msg.content,
            })
        elif msg.role == "assistant" and msg.tool_calls:
            entry: dict[str, Any] = {"role": "assistant"}
            if msg.content:
                entry["content"] = msg.content
            else:
                entry["content"] = None
            entry["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.name,
                        "arguments": json.dumps(tc.arguments),
                    },
                }
                for tc in msg.tool_calls
            ]
            result.append(entry)
        elif msg.role in ("user", "assistant"):
            result.append({"role": msg.role, "content": msg.content})
    return result


def _tools_to_ollama(tools: list[dict[str, Any]]) -> list[dict]:
    """Convert tool schemas to OpenAI function calling format."""
    result = []
    for tool in tools:
        result.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"],
            },
        })
    return result


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider — uses OpenAI-compatible API."""

    def __init__(self, model: str = "qwen2.5:0.5b") -> None:
        self.model = model
        self.client = openai.OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",  # Ollama doesn't need a real key
        )

    def chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        system: str = "",
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": _messages_to_ollama(messages, system),
        }
        if tools:
            kwargs["tools"] = _tools_to_ollama(tools)

        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        message = choice.message

        tool_calls: list[ToolCall] = []
        if message.tool_calls:
            for tc in message.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {}
                tool_calls.append(
                    ToolCall(id=tc.id, name=tc.function.name, arguments=args)
                )

        return LLMResponse(
            content=message.content or "",
            tool_calls=tool_calls,
            stop_reason=choice.finish_reason,
        )

    async def stream_chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        system: str = "",
    ) -> AsyncIterator[str]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": _messages_to_ollama(messages, system),
            "stream": True,
        }
        # Don't pass tools in streaming mode for compatibility
        stream = self.client.chat.completions.create(**kwargs)
        for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield delta.content

    def get_model_name(self) -> str:
        return f"Ollama ({self.model}) — Local & Free"
