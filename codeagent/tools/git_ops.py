"""Tool: Git operations."""

from __future__ import annotations
import subprocess
from typing import Any

from .base import BaseTool


class GitOpsTool(BaseTool):
    name = "git_ops"
    description = (
        "Perform git operations: status, diff, log, add, commit, branch, checkout. "
        "Runs git commands in the current working directory."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["status", "diff", "log", "add", "commit", "branch", "checkout", "stash", "show"],
                "description": "The git operation to perform.",
            },
            "args": {
                "type": "string",
                "description": "Additional arguments for the git command. E.g. '-m \"commit message\"' for commit, file paths for add, branch name for checkout.",
            },
        },
        "required": ["operation"],
    }

    # Operations that are always safe (read-only)
    SAFE_OPS = {"status", "diff", "log", "branch", "show"}

    def execute(self, operation: str, args: str = "", **_: Any) -> str:
        command = f"git {operation}"
        if args:
            command += f" {args}"

        # Block force-push and other dangerous operations
        if "--force" in args or "-f" in args:
            if operation in ("push",):
                return "Error: Force push blocked for safety. Use the terminal tool directly if you really need this."

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                # Git often writes informational messages to stderr
                output += result.stderr

            output = output.strip()
            if not output:
                output = "(no output)"

            if len(output) > 15000:
                output = output[:15000] + "\n... (output truncated)"

            return f"$ {command}\n{output}"

        except subprocess.TimeoutExpired:
            return f"Error: git command timed out"
        except Exception as e:
            return f"Error: {e}"
