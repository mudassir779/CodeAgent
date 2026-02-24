"""Loading spinner for LLM calls."""

from __future__ import annotations
from contextlib import contextmanager
from typing import Generator

from rich.live import Live
from rich.spinner import Spinner as RichSpinner
from rich.text import Text

from .console import console


@contextmanager
def Spinner(message: str = "Thinking...") -> Generator[None, None, None]:
    """Context manager that shows a spinner while the LLM is working."""
    spinner = RichSpinner("dots", text=Text(f" {message}", style="info"))
    with Live(spinner, console=console, refresh_per_second=10, transient=True):
        yield
