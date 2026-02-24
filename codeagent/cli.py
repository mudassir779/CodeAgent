"""CLI entry point using Click."""

from __future__ import annotations
import click
from . import __version__


@click.command()
@click.version_option(__version__, prog_name="CodeAgent")
@click.option(
    "--model", "-m",
    type=click.Choice(["claude", "openai", "ollama", "demo"], case_sensitive=False),
    default=None,
    help="LLM provider: claude, openai, ollama (free local), or demo.",
)
@click.argument("message", nargs=-1)
def main(model: str | None, message: tuple[str, ...]) -> None:
    """CodeAgent - AI coding assistant in your terminal.

    Start an interactive session, or pass a MESSAGE for one-shot mode.

    Examples:

        codeagent                        # interactive session
        codeagent --model openai         # use OpenAI
        codeagent "explain this code"    # one-shot
        codeagent demo                   # run client demo
    """
    # Check for demo command first (no API key needed)
    if message and message[0].lower() == "demo":
        from .demo import run_demo
        run_demo()
        return

    from .app import Agent

    agent = Agent(provider_name=model)

    if message:
        agent.run_oneshot(" ".join(message))
    else:
        agent.run_interactive()


if __name__ == "__main__":
    main()
