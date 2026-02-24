"""Tool: Search for patterns in code files."""

from __future__ import annotations
import fnmatch
import re
from pathlib import Path
from typing import Any

from .base import BaseTool

# Skip these directories when searching
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".next", "dist", "build", ".eggs", "*.egg-info",
}


class CodeSearchTool(BaseTool):
    name = "code_search"
    description = (
        "Search for a text pattern (regex supported) across files in a directory. "
        "Returns matching lines with file paths and line numbers. "
        "Like grep/ripgrep for codebases."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "The regex pattern to search for.",
            },
            "path": {
                "type": "string",
                "description": "Directory to search in. Defaults to current directory.",
            },
            "glob": {
                "type": "string",
                "description": "File glob pattern to filter files, e.g. '*.py' or '*.ts'. Optional.",
            },
            "case_insensitive": {
                "type": "boolean",
                "description": "Case-insensitive search. Default false.",
            },
        },
        "required": ["pattern"],
    }

    def execute(
        self,
        pattern: str,
        path: str = ".",
        glob: str = "",
        case_insensitive: bool = False,
        **_: Any,
    ) -> str:
        search_path = Path(path).expanduser().resolve()
        if not search_path.exists():
            return f"Error: Path not found: {search_path}"

        flags = re.IGNORECASE if case_insensitive else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            return f"Error: Invalid regex pattern: {e}"

        matches: list[str] = []
        max_matches = 100

        for file_path in self._walk_files(search_path, glob):
            if len(matches) >= max_matches:
                break
            try:
                text = file_path.read_text(encoding="utf-8", errors="replace")
                for i, line in enumerate(text.splitlines(), 1):
                    if regex.search(line):
                        rel = file_path.relative_to(search_path)
                        matches.append(f"{rel}:{i}: {line.rstrip()}")
                        if len(matches) >= max_matches:
                            break
            except (PermissionError, OSError):
                continue

        if not matches:
            return f"No matches found for pattern '{pattern}' in {search_path}"

        header = f"Found {len(matches)} match(es)"
        if len(matches) >= max_matches:
            header += f" (limited to {max_matches})"
        return header + "\n\n" + "\n".join(matches)

    @staticmethod
    def _walk_files(root: Path, glob_pattern: str) -> list[Path]:
        files: list[Path] = []
        for item in root.rglob("*"):
            if any(part in SKIP_DIRS for part in item.parts):
                continue
            if item.is_file():
                if glob_pattern and not fnmatch.fnmatch(item.name, glob_pattern):
                    continue
                # Skip binary files by extension
                if item.suffix in (".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".zip", ".tar", ".gz", ".exe", ".dll", ".so", ".dylib"):
                    continue
                files.append(item)
        return files
