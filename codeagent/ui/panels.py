"""Output formatting: panels, code blocks, tool results."""

from __future__ import annotations

from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from .console import console


def print_welcome(model_name: str) -> None:
    """Print the welcome banner."""
    welcome = Text()
    welcome.append("CodeAgent", style="bold cyan")
    welcome.append(" - AI Coding Assistant\n", style="dim")
    welcome.append(f"Model: {model_name}\n", style="info")
    welcome.append("Type ", style="dim")
    welcome.append("/help", style="bold")
    welcome.append(" for commands, ", style="dim")
    welcome.append("/quit", style="bold")
    welcome.append(" to exit", style="dim")
    console.print(Panel(welcome, border_style="cyan", padding=(0, 1)))


def print_assistant(text: str) -> None:
    """Print the assistant's text response as markdown."""
    if text.strip():
        console.print()
        console.print(Markdown(text))
        console.print()


def print_tool_call(name: str, arguments: dict) -> None:
    """Print a tool call notification."""
    args_summary = ", ".join(f"{k}={_truncate(str(v))}" for k, v in arguments.items())
    console.print(
        Text.assemble(
            ("  Tool: ", "tool.name"),
            (name, "bold yellow"),
            ("(", "dim"),
            (args_summary, "dim"),
            (")", "dim"),
        )
    )


def print_tool_result(name: str, result: str) -> None:
    """Print a tool result in a panel."""
    # Truncate very long results for display
    display = result if len(result) <= 2000 else result[:2000] + "\n... (truncated)"
    console.print(
        Panel(
            display,
            title=f"[tool.name]{name}[/tool.name]",
            border_style="dim",
            padding=(0, 1),
        )
    )


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[error]Error:[/error] {message}")


def print_info(message: str) -> None:
    """Print an info message."""
    console.print(f"[info]{message}[/info]")


def _truncate(s: str, max_len: int = 60) -> str:
    """Truncate a string for display."""
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."
