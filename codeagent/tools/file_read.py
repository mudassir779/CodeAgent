"""Tool: Read file contents."""

from __future__ import annotations
from pathlib import Path
from typing import Any

from .base import BaseTool


class FileReadTool(BaseTool):
    name = "file_read"
    description = (
        "Read the contents of a file. Returns the file text with line numbers. "
        "Use this before editing a file to understand its contents."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Absolute or relative path to the file to read.",
            },
            "offset": {
                "type": "integer",
                "description": "Line number to start reading from (1-based). Optional.",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of lines to read. Optional.",
            },
        },
        "required": ["path"],
    }

    def execute(self, path: str, offset: int = 1, limit: int = 0, **_: Any) -> str:
        file_path = Path(path).expanduser().resolve()
        if not file_path.exists():
            return f"Error: File not found: {file_path}"
        if not file_path.is_file():
            return f"Error: Not a file: {file_path}"

        try:
            text = file_path.read_text(encoding="utf-8", errors="replace")
        except PermissionError:
            return f"Error: Permission denied: {file_path}"

        lines = text.splitlines()
        start = max(0, offset - 1)
        end = start + limit if limit > 0 else len(lines)
        selected = lines[start:end]

        numbered = [f"{start + i + 1:>5}\t{line}" for i, line in enumerate(selected)]
        header = f"File: {file_path} ({len(lines)} lines total)"
        return header + "\n" + "\n".join(numbered)
