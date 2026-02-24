"""Main agent loop — the brain of CodeAgent."""

from __future__ import annotations

from .config import config
from .constants import SYSTEM_PROMPT, MAX_TOOL_ROUNDS, MAX_HISTORY_MESSAGES
from .llm import get_provider, Message, ToolCall, ToolResult, LLMResponse
from .llm.base import BaseLLMProvider
from .tools import registry
from .ui import (
    console,
    print_tool_call,
    print_tool_result,
    print_error,
    print_welcome,
    print_assistant,
    Spinner,
)
from .ui.panels import print_info


class Agent:
    """Interactive coding agent that loops between user input, LLM, and tools."""

    def __init__(self, provider_name: str | None = None) -> None:
        self.provider_name = provider_name or config.default_provider
        self.provider: BaseLLMProvider = self._init_provider(self.provider_name)
        self.history: list[Message] = []

    def _init_provider(self, name: str) -> BaseLLMProvider:
        error = config.validate_provider(name)
        if error:
            print_error(error)
            raise SystemExit(1)
        return get_provider(name)

    def switch_provider(self, name: str) -> None:
        """Switch to a different LLM provider mid-conversation."""
        error = config.validate_provider(name)
        if error:
            print_error(error)
            return
        self.provider_name = name
        self.provider = get_provider(name)
        print_info(f"Switched to {self.provider.get_model_name()}")

    def run_interactive(self) -> None:
        """Start the interactive REPL loop."""
        from prompt_toolkit import PromptSession
        from prompt_toolkit.history import InMemoryHistory

        print_welcome(self.provider.get_model_name())
        session: PromptSession = PromptSession(history=InMemoryHistory())

        while True:
            try:
                user_input = session.prompt("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[info]Goodbye![/info]")
                break

            if not user_input:
                continue

            if self._handle_command(user_input):
                continue

            self._process_message(user_input)

    def run_oneshot(self, message: str) -> None:
        """Process a single message and exit."""
        self._process_message(message)

    def _handle_command(self, text: str) -> bool:
        """Handle slash commands. Returns True if it was a command."""
        if not text.startswith("/"):
            return False

        parts = text.split(maxsplit=1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ("/quit", "/exit", "/q"):
            console.print("[info]Goodbye![/info]")
            raise SystemExit(0)
        elif cmd == "/help":
            self._print_help()
        elif cmd == "/model":
            if arg:
                self.switch_provider(arg)
            else:
                console.print(f"[info]Current model: {self.provider.get_model_name()}[/info]")
                console.print("[dim]Usage: /model claude  or  /model openai[/dim]")
        elif cmd == "/clear":
            self.history.clear()
            print_info("Conversation history cleared.")
        elif cmd == "/tools":
            names = registry.list_names()
            console.print(f"[info]Available tools ({len(names)}):[/info]")
            for name in names:
                console.print(f"  [tool.name]{name}[/tool.name]")
        else:
            console.print(f"[warning]Unknown command: {cmd}[/warning]")

        return True

    def _print_help(self) -> None:
        console.print(
            "\n".join([
                "[bold]Commands:[/bold]",
                "  [bold]/model[/bold] <provider>  Switch model (claude, openai)",
                "  [bold]/clear[/bold]             Clear conversation history",
                "  [bold]/tools[/bold]             List available tools",
                "  [bold]/help[/bold]              Show this help",
                "  [bold]/quit[/bold]              Exit CodeAgent",
            ])
        )

    def _process_message(self, user_input: str) -> None:
        """Send a user message through the agent loop."""
        self.history.append(Message(role="user", content=user_input))
        self._trim_history()

        tool_schemas = registry.get_schemas()

        for _ in range(MAX_TOOL_ROUNDS):
            with Spinner("Thinking..."):
                response = self.provider.chat(
                    messages=self.history,
                    tools=tool_schemas,
                    system=SYSTEM_PROMPT,
                )

            # Show any text content
            if response.content:
                print_assistant(response.content)

            # If no tool calls, we're done
            if not response.has_tool_calls:
                self.history.append(Message(role="assistant", content=response.content))
                break

            # Record assistant message with tool calls
            self.history.append(
                Message(
                    role="assistant",
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )

            # Execute each tool call
            for tc in response.tool_calls:
                print_tool_call(tc.name, tc.arguments)
                result = registry.execute(tc.name, tc.arguments)
                print_tool_result(tc.name, result)

                # Add tool result to history
                self.history.append(
                    Message(
                        role="tool",
                        content=result,
                        tool_call_id=tc.id,
                        name=tc.name,
                    )
                )
        else:
            print_error(f"Reached maximum tool rounds ({MAX_TOOL_ROUNDS}). Stopping.")

    def _trim_history(self) -> None:
        """Keep conversation history under the limit."""
        if len(self.history) > MAX_HISTORY_MESSAGES:
            # Keep the most recent messages, preserving pairs
            self.history = self.history[-MAX_HISTORY_MESSAGES:]
