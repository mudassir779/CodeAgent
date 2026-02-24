"""Configuration loading from .env and environment."""

import os
from pathlib import Path
from dotenv import load_dotenv


def _find_env_file() -> Path | None:
    """Walk up from cwd looking for .env."""
    current = Path.cwd()
    for directory in [current, *current.parents]:
        env_path = directory / ".env"
        if env_path.exists():
            return env_path
    return None


class Config:
    """Application configuration loaded from environment."""

    def __init__(self) -> None:
        env_file = _find_env_file()
        if env_file:
            load_dotenv(env_file)

        self.anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.default_provider: str = os.getenv("CODEAGENT_DEFAULT_PROVIDER", "claude")

    def has_anthropic(self) -> bool:
        return bool(self.anthropic_api_key and self.anthropic_api_key != "sk-ant-xxxxx")

    def has_openai(self) -> bool:
        return bool(self.openai_api_key and self.openai_api_key != "sk-xxxxx")

    def validate_provider(self, provider: str) -> str | None:
        """Return an error message if the provider can't be used, else None."""
        if provider in ("demo", "ollama"):
            return None  # No API key needed
        if provider == "claude" and not self.has_anthropic():
            return "ANTHROPIC_API_KEY not set. Add it to your .env file."
        if provider == "openai" and not self.has_openai():
            return "OPENAI_API_KEY not set. Add it to your .env file."
        if provider not in ("claude", "openai", "ollama", "demo"):
            return f"Unknown provider '{provider}'. Use 'claude', 'openai', 'ollama', or 'demo'."
        return None


config = Config()
