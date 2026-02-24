"""Tool: List directory contents."""

from __future__ import annotations
from pathlib import Path
from typing import Any

from .base import BaseTool


class DirectoryListTool(BaseTool):
    name = "directory_list"
    description = (
        "List files and directories at a given path. "
        "Shows file sizes and types. Use to explore project structure."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Directory path to list. Defaults to current directory.",
            },
            "recursive": {
                "type": "boolean",
                "description": "If true, list recursively (up to 3 levels). Default false.",
            },
        },
        "required": [],
    }

    def execute(self, path: str = ".", recursive: bool = False, **_: Any) -> str:
        dir_path = Path(path).expanduser().resolve()
        if not dir_path.exists():
            return f"Error: Path not found: {dir_path}"
        if not dir_path.is_dir():
            return f"Error: Not a directory: {dir_path}"

        lines: list[str] = [f"Directory: {dir_path}\n"]
        try:
            self._list_dir(dir_path, lines, depth=0, max_depth=3 if recursive else 1)
        except PermissionError:
            lines.append("(permission denied for some entries)")

        return "\n".join(lines)

    def _list_dir(
        self, path: Path, lines: list[str], depth: int, max_depth: int
    ) -> None:
        if depth >= max_depth:
            return
        indent = "  " * depth
        try:
            entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except PermissionError:
            lines.append(f"{indent}(permission denied)")
            return

        for entry in entries:
            if entry.name.startswith(".") and depth == 0:
                continue  # skip hidden files at top level for cleaner output
            if entry.is_dir():
                lines.append(f"{indent}{entry.name}/")
                if depth + 1 < max_depth:
                    self._list_dir(entry, lines, depth + 1, max_depth)
            else:
                size = self._human_size(entry.stat().st_size)
                lines.append(f"{indent}{entry.name}  ({size})")

    @staticmethod
    def _human_size(size: int) -> str:
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.0f}{unit}" if unit == "B" else f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
