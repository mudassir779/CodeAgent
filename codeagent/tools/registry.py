"""Tool registry — collects all tools and dispatches execution."""

from __future__ import annotations
from typing import Any

from .base import BaseTool


class ToolRegistry:
    """Central registry of all available tools."""

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> BaseTool | None:
        return self._tools.get(name)

    def get_schemas(self) -> list[dict[str, Any]]:
        """Return all tool schemas for the LLM."""
        return [tool.to_schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: dict[str, Any]) -> str:
        """Execute a tool by name. Returns result string."""
        tool = self._tools.get(name)
        if tool is None:
            return f"Error: Unknown tool '{name}'"
        try:
            return tool.execute(**arguments)
        except Exception as e:
            return f"Error executing {name}: {e}"

    def list_names(self) -> list[str]:
        return list(self._tools.keys())


# Global registry instance — tools register themselves on import
registry = ToolRegistry()


def _register_all_tools() -> None:
    """Import all tool modules so they register with the global registry."""
    from .file_read import FileReadTool
    from .file_write import FileWriteTool
    from .file_edit import FileEditTool
    from .directory_list import DirectoryListTool
    from .code_search import CodeSearchTool
    from .terminal import TerminalTool
    from .git_ops import GitOpsTool

    for tool_cls in [
        FileReadTool,
        FileWriteTool,
        FileEditTool,
        DirectoryListTool,
        CodeSearchTool,
        TerminalTool,
        GitOpsTool,
    ]:
        registry.register(tool_cls())


_register_all_tools()
