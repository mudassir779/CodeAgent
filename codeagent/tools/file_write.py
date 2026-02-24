"""Tool: Write/create files."""

from __future__ import annotations
from pathlib import Path
from typing import Any

from .base import BaseTool


class FileWriteTool(BaseTool):
    name = "file_write"
    description = (
        "Write content to a file. Creates the file (and parent directories) if it "
        "does not exist, or overwrites if it does. Use file_edit for surgical changes."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to write.",
            },
            "content": {
                "type": "string",
                "description": "The full content to write to the file.",
            },
        },
        "required": ["path", "content"],
    }

    def execute(self, path: str, content: str, **_: Any) -> str:
        file_path = Path(path).expanduser().resolve()
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            lines = content.count("\n") + (1 if content and not content.endswith("\n") else 0)
            return f"Written {lines} lines to {file_path}"
        except PermissionError:
            return f"Error: Permission denied: {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"
