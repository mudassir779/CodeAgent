"""Rich console setup with custom theme."""

from rich.console import Console
from rich.theme import Theme

theme = Theme({
    "agent": "bold cyan",
    "user": "bold green",
    "tool.name": "bold yellow",
    "tool.result": "dim",
    "error": "bold red",
    "info": "dim cyan",
    "success": "bold green",
    "warning": "bold yellow",
})

console = Console(theme=theme)
