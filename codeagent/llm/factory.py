"""Factory to create LLM providers by name."""

from __future__ import annotations

from .base import BaseLLMProvider


def get_provider(name: str) -> BaseLLMProvider:
    """Return an LLM provider instance by name.

    Args:
        name: "claude", "openai", or "demo"

    Raises:
        ValueError: If provider name is unknown.
    """
    if name == "claude":
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider()
    elif name == "openai":
        from .openai_provider import OpenAIProvider
        return OpenAIProvider()
    elif name == "ollama":
        from .ollama_provider import OllamaProvider
        return OllamaProvider()
    elif name == "demo":
        from .mock_provider import MockProvider
        return MockProvider()
    else:
        raise ValueError(f"Unknown provider: '{name}'. Use 'claude', 'openai', 'ollama', or 'demo'.")
