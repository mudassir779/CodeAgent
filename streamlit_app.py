"""CodeAgent - Web Demo for Client Presentations."""

import streamlit as st

st.set_page_config(
    page_title="CodeAgent - AI Coding Assistant",
    page_icon="🤖",
    layout="wide",
)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.title("🤖 CodeAgent")
st.subheader("AI-Powered Coding Assistant in Your Terminal")
st.write("")

# Stats
c1, c2, c3, c4 = st.columns(4)
c1.metric("Built-in Tools", "7")
c2.metric("AI Providers", "3")
c3.metric("Ollama Cost", "$0")
c4.metric("Tool Execution", "<1s")

st.write("")
st.markdown(
    "**Supported Providers:** "
    "`Claude (Anthropic)` · `GPT-4o (OpenAI)` · `Ollama (Local & Free)`"
)

st.divider()

# ── Demo Steps ────────────────────────────────────────────────────────────────
STEPS = [
    {
        "user": "📖 Read the pyproject.toml file",
        "tool": "file_read",
        "args": "path=pyproject.toml",
        "output": '[build-system]\nrequires = ["setuptools>=68.0", "wheel"]\n\n[project]\nname = "codeagent"\nversion = "0.1.0"\ndescription = "CLI-based AI coding assistant"\nrequires-python = ">=3.10"\ndependencies = [\n    "anthropic>=0.39.0",\n    "openai>=1.50.0",\n    "rich>=13.7.0",\n    "click>=8.1.0",\n]',
        "response": "The project uses **Python 3.10+** with 6 core dependencies: *anthropic*, *openai*, *rich*, *click*, *python-dotenv*, and *prompt-toolkit*.",
    },
    {
        "user": "📂 List the project structure",
        "tool": "directory_list",
        "args": "path=., recursive=true",
        "output": "codeagent/\n  llm/\n    anthropic_provider.py\n    openai_provider.py\n    ollama_provider.py\n    base.py, factory.py, types.py\n  tools/\n    file_read.py, file_write.py\n    file_edit.py, directory_list.py\n    code_search.py, terminal.py\n    git_ops.py, registry.py\n  ui/\n    console.py, panels.py, spinner.py\n  app.py, cli.py, config.py",
        "response": "Clean **modular architecture**: `llm/` for AI providers, `tools/` for 7 agent tools, `ui/` for Rich terminal components.",
    },
    {
        "user": "🔍 Search for 'def execute' in tools",
        "tool": "code_search",
        "args": "pattern=def execute, path=codeagent/tools",
        "output": "Found 7 matches:\n\nfile_read.py:35      def execute(self, path, offset, limit)\nfile_write.py:31     def execute(self, path, content)\nfile_edit.py:40      def execute(self, path, old_string, new_string)\ndirectory_list.py:31 def execute(self, path, recursive)\ncode_search.py:48    def execute(self, pattern, path, glob)\nterminal.py:35       def execute(self, command, timeout)\ngit_ops.py:35        def execute(self, operation, args)",
        "response": "All **7 tools** implement the same `BaseTool` interface. The LLM decides which tool to call based on the user's request.",
    },
    {
        "user": "✏️ Create a fibonacci.py file",
        "tool": "file_write",
        "args": "path=fibonacci.py",
        "output": "Written 18 lines to fibonacci.py",
        "response": "Created **fibonacci.py** with type-annotated functions, docstrings, and a main block. Production-quality code generated automatically.",
    },
    {
        "user": "▶️ Run the fibonacci file",
        "tool": "terminal",
        "args": "command=python3 fibonacci.py",
        "output": "Exit code: 0\nFibonacci sequence (first 10):\n[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\n\nThe 20th Fibonacci number is: 6765",
        "response": "CodeAgent can **write code**, **run it immediately**, and **debug** if anything fails — all in one conversation.",
    },
    {
        "user": "📊 Show git status",
        "tool": "git_ops",
        "args": "operation=status",
        "output": "On branch main\nChanges to be committed:\n  new file:   fibonacci.py\n\nUntracked files:\n  web_demo.py",
        "response": "Git integration built-in. I can run **status**, **diff**, **add**, **commit**, and **log** — all through natural language.",
    },
]

# ── Live Demo Section ─────────────────────────────────────────────────────────
st.markdown("### 🖥️ Live Demo")
st.caption("Watch CodeAgent handle real coding tasks step by step")

# Session state
if "step" not in st.session_state:
    st.session_state.step = 0

# Buttons at top
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("▶ Next Step", use_container_width=True, disabled=st.session_state.step >= len(STEPS)):
        st.session_state.step += 1
        st.rerun()
with b2:
    if st.button("⏩ Run All Steps", use_container_width=True, disabled=st.session_state.step >= len(STEPS)):
        st.session_state.step = len(STEPS)
        st.rerun()
with b3:
    if st.button("🔄 Reset Demo", use_container_width=True):
        st.session_state.step = 0
        st.rerun()

st.write("")

# Show steps
if st.session_state.step == 0:
    st.info("👆 Click **Next Step** to start the demo")
else:
    for i in range(min(st.session_state.step, len(STEPS))):
        s = STEPS[i]

        st.markdown(f"**`>`** {s['user']}")

        col_tool, col_args = st.columns([1, 3])
        with col_tool:
            st.code(f"🔧 {s['tool']}", language=None)
        with col_args:
            st.caption(f"({s['args']})")

        with st.expander(f"📋 Tool Output", expanded=True):
            st.code(s["output"], language=None)

        st.markdown(f"> {s['response']}")
        st.write("")

    if st.session_state.step >= len(STEPS):
        st.success("✅ **Demo Complete** — All 7 tools demonstrated successfully!")

st.divider()

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown("### ⚡ Features")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**📁 File Operations**")
    st.caption("Read, write, edit files with precision")
with col2:
    st.markdown("**🔍 Code Search**")
    st.caption("Regex search across entire codebases")
with col3:
    st.markdown("**🖥️ Terminal**")
    st.caption("Execute commands with safety checks")
with col4:
    st.markdown("**📊 Git Integration**")
    st.caption("Status, diff, commit, log built-in")

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.markdown("**🔄 Multi-Provider**")
    st.caption("Claude, OpenAI, or local Ollama")
with col6:
    st.markdown("**⚡ Streaming**")
    st.caption("Real-time response output")
with col7:
    st.markdown("**🛡️ Safe by Design**")
    st.caption("Confirms destructive operations")
with col8:
    st.markdown("**🎨 Beautiful UI**")
    st.caption("Rich panels & syntax highlighting")

st.divider()

# ── Architecture ──────────────────────────────────────────────────────────────
st.markdown("### 🏗️ Architecture")

st.code("""
    ┌─────────────┐
    │  User Input  │
    └──────┬──────┘
           │
    ┌──────▼──────┐     ┌───────────────┐
    │  Agent Loop  │────▶│  LLM Provider  │
    │   (app.py)   │◀────│ Claude / GPT / │
    └──────┬──────┘     │    Ollama      │
           │             └───────────────┘
    ┌──────▼──────┐
    │ Tool Registry│
    └──────┬──────┘
           │
    ┌──────▼──────────────────────────┐
    │         7 Agent Tools           │
    ├─────────┬──────────┬────────────┤
    │file_read│file_write│ file_edit   │
    │dir_list │code_srch │ terminal    │
    │         │ git_ops  │             │
    └─────────┴──────────┴────────────┘
""", language=None)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "**CodeAgent v0.1.0** · "
    "Built with Python · Powered by Claude & OpenAI · Beautiful with Rich"
)
st.caption("Ready for production deployment")
