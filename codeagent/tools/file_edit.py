"""Tool: Edit existing files with string replacement."""

from __future__ import annotations
from pathlib import Path
from typing import Any

from .base import BaseTool


class FileEditTool(BaseTool):
    name = "file_edit"
    description = (
        "Edit a file by replacing an exact string with a new string. "
        "The old_string must match exactly (including whitespace/indentation). "
        "Read the file first to get the exact content."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the file to edit.",
            },
            "old_string": {
                "type": "string",
                "description": "The exact string to find and replace.",
            },
            "new_string": {
                "type": "string",
                "description": "The replacement string.",
            },
            "replace_all": {
                "type": "boolean",
                "description": "If true, replace all occurrences. Default false.",
            },
        },
        "required": ["path", "old_string", "new_string"],
    }

    def execute(
        self,
        path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False,
        **_: Any,
    ) -> str:
        file_path = Path(path).expanduser().resolve()
        if not file_path.exists():
            return f"Error: File not found: {file_path}"

        try:
            content = file_path.read_text(encoding="utf-8")
        except PermissionError:
            return f"Error: Permission denied: {file_path}"

        count = content.count(old_string)
        if count == 0:
            return "Error: old_string not found in file. Read the file first to get the exact text."
        if count > 1 and not replace_all:
            return (
                f"Error: old_string found {count} times. "
                "Set replace_all=true or provide more context to make it unique."
            )

        if replace_all:
            new_content = content.replace(old_string, new_string)
            replacements = count
        else:
            new_content = content.replace(old_string, new_string, 1)
            replacements = 1

        file_path.write_text(new_content, encoding="utf-8")
        return f"Replaced {replacements} occurrence(s) in {file_path}"
