"""Tool: Execute shell commands."""

from __future__ import annotations
import subprocess
from typing import Any

from .base import BaseTool

# Commands that are always blocked
BLOCKED_COMMANDS = {"rm -rf /", "mkfs", "dd if=", ":(){:|:&};:"}


class TerminalTool(BaseTool):
    name = "terminal"
    description = (
        "Execute a shell command in the terminal and return its output. "
        "Use for running builds, tests, installing packages, git commands, etc. "
        "Commands run in the current working directory."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute.",
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds. Default 60.",
            },
        },
        "required": ["command"],
    }

    def execute(self, command: str, timeout: int = 60, **_: Any) -> str:
        # Safety check
        for blocked in BLOCKED_COMMANDS:
            if blocked in command:
                return f"Error: Blocked dangerous command: {command}"

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=min(timeout, 300),  # Cap at 5 minutes
                cwd=None,  # Use current working directory
            )
            output_parts: list[str] = []
            if result.stdout:
                output_parts.append(result.stdout)
            if result.stderr:
                output_parts.append(f"[stderr]\n{result.stderr}")

            output = "\n".join(output_parts).strip()
            if not output:
                output = "(no output)"

            # Truncate very long output
            if len(output) > 20000:
                output = output[:20000] + "\n... (output truncated)"

            status = f"Exit code: {result.returncode}"
            return f"{status}\n{output}"

        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after {timeout}s"
        except Exception as e:
            return f"Error executing command: {e}"
