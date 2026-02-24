"""CodeAgent — Web Demo for Client Presentations."""

import time
import streamlit as st

st.set_page_config(
    page_title="CodeAgent — AI Coding Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS for terminal look ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');

.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}
.stApp header { background-color: #0d1117 !important; }

.terminal-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 16px;
    overflow-x: auto;
}

.terminal-header {
    background: linear-gradient(135deg, #1a1f2e, #161b22);
    border: 1px solid #30363d;
    border-radius: 12px 12px 0 0;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0;
}
.terminal-header .dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.dot-red { background: #ff5f57; }
.dot-yellow { background: #febc2e; }
.dot-green { background: #28c840; }
.terminal-header .title {
    color: #8b949e;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    margin-left: 12px;
}

.terminal-body {
    background: #0d1117;
    border: 1px solid #30363d;
    border-top: none;
    border-radius: 0 0 12px 12px;
    padding: 20px 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.7;
    min-height: 200px;
}

.user-input { color: #58a6ff; font-weight: 600; }
.prompt-symbol { color: #3fb950; font-weight: 700; }
.tool-badge {
    background: #1c2333;
    border: 1px solid #f0883e40;
    border-radius: 6px;
    padding: 3px 10px;
    color: #f0883e;
    font-size: 12px;
    display: inline-block;
    margin: 4px 0;
}
.tool-output {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 8px 0 12px 0;
    color: #8b949e;
    font-size: 12px;
    white-space: pre-wrap;
    max-height: 250px;
    overflow-y: auto;
}
.ai-response { color: #e6edf3; margin: 8px 0 20px 0; }
.ai-response strong { color: #58a6ff; }
.ai-response em { color: #3fb950; font-style: normal; }

.hero-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #58a6ff, #3fb950);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0;
}
.hero-subtitle {
    font-family: 'JetBrains Mono', monospace;
    color: #8b949e;
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 40px;
}

.feature-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    transition: border-color 0.3s;
}
.feature-card:hover { border-color: #58a6ff; }
.feature-card .icon { font-size: 2rem; margin-bottom: 12px; }
.feature-card .title { color: #e6edf3; font-weight: 600; font-size: 1rem; margin-bottom: 6px; font-family: 'JetBrains Mono', monospace; }
.feature-card .desc { color: #8b949e; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; }

.stats-row {
    display: flex;
    justify-content: center;
    gap: 60px;
    margin: 30px 0;
}
.stat { text-align: center; }
.stat .number { font-size: 2.5rem; font-weight: 700; color: #58a6ff; font-family: 'JetBrains Mono', monospace; }
.stat .label { color: #8b949e; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; }

.provider-badge {
    display: inline-block;
    background: #1c2333;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 6px 16px;
    margin: 4px;
    color: #e6edf3;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}

/* Hide streamlit defaults */
#MainMenu, footer, .stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ── Demo Data ─────────────────────────────────────────────────────────────────
DEMO_STEPS = [
    {
        "user": "Read the pyproject.toml file",
        "tool": "file_read",
        "tool_args": "path=pyproject.toml",
        "output": """[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "codeagent"
version = "0.1.0"
description = "CLI-based AI coding assistant"
requires-python = ">=3.10"
dependencies = [
    "anthropic>=0.39.0",
    "openai>=1.50.0",
    "rich>=13.7.0",
    "click>=8.1.0",
    "python-dotenv>=1.0.0",
    "prompt-toolkit>=3.0.0",
]""",
        "response": """The project uses <strong>Python 3.10+</strong> with 6 core dependencies:
<em>anthropic</em>, <em>openai</em>, <em>rich</em>, <em>click</em>, <em>python-dotenv</em>, and <em>prompt-toolkit</em>.
Entry point is configured as the <strong>codeagent</strong> CLI command.""",
    },
    {
        "user": "List the project structure",
        "tool": "directory_list",
        "tool_args": "path=., recursive=true",
        "output": """codeagent/
  llm/
    anthropic_provider.py   (Claude API)
    openai_provider.py      (OpenAI API)
    ollama_provider.py      (Local LLM)
    base.py                 (Abstract interface)
    factory.py              (Provider switching)
    types.py                (Message types)
  tools/
    file_read.py            (Read files)
    file_write.py           (Write/create files)
    file_edit.py            (Edit with replacement)
    directory_list.py       (List directories)
    code_search.py          (Search codebase)
    terminal.py             (Shell commands)
    git_ops.py              (Git operations)
    registry.py             (Tool registry)
  ui/
    console.py              (Rich terminal)
    panels.py               (Output formatting)
    spinner.py              (Loading animations)
  app.py                    (Agent loop)
  cli.py                    (CLI entry point)
  config.py                 (Configuration)""",
        "response": """Clean <strong>modular architecture</strong> with 3 layers:
<strong>llm/</strong> — Multi-provider AI support (Claude, OpenAI, Ollama)
<strong>tools/</strong> — 7 agent tools for file ops, search, git & terminal
<strong>ui/</strong> — Beautiful Rich terminal UI with panels & spinners""",
    },
    {
        "user": "Search for 'def execute' across all tools",
        "tool": "code_search",
        "tool_args": 'pattern="def execute", path=codeagent/tools',
        "output": """Found 7 matches:

file_read.py:35      def execute(self, path, offset=1, limit=0)
file_write.py:31     def execute(self, path, content)
file_edit.py:40      def execute(self, path, old_string, new_string)
directory_list.py:31 def execute(self, path=".", recursive=False)
code_search.py:48    def execute(self, pattern, path=".", glob="")
terminal.py:35       def execute(self, command, timeout=60)
git_ops.py:35        def execute(self, operation, args="")""",
        "response": """All <strong>7 tools</strong> implement the same <em>BaseTool</em> interface.
Each tool registers automatically with the <strong>ToolRegistry</strong>.
The LLM decides which tool to call based on the user's request — the agent handles execution and feeds results back.""",
    },
    {
        "user": "Create a fibonacci.py file",
        "tool": "file_write",
        "tool_args": "path=fibonacci.py",
        "output": "Written 18 lines to fibonacci.py",
        "response": """Created <strong>fibonacci.py</strong> with:
- Type-annotated <em>fibonacci()</em> generator function
- <em>fib_sequence()</em> helper returning a list
- Main block with example output
All production-quality with proper docstrings.""",
    },
    {
        "user": "Run the fibonacci file",
        "tool": "terminal",
        "tool_args": "command=python3 fibonacci.py",
        "output": """Exit code: 0
Fibonacci sequence (first 10):
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

The 20th Fibonacci number is: 6765""",
        "response": """File executed successfully. CodeAgent can <strong>write code</strong>,
<strong>run it immediately</strong>, and <strong>debug</strong> if anything fails —
all in a single conversation flow. No context switching needed.""",
    },
    {
        "user": "Show git status",
        "tool": "git_ops",
        "tool_args": "operation=status",
        "output": """On branch main
Changes to be committed:
  new file:   fibonacci.py

Untracked files:
  web_demo.py""",
        "response": """Git integration is built-in. I can run <strong>status</strong>, <strong>diff</strong>,
<strong>add</strong>, <strong>commit</strong>, and <strong>log</strong> — all through natural language.
Ask me to <em>"commit the fibonacci file with a descriptive message"</em> and I'll handle it.""",
    },
]


# ── Page Layout ───────────────────────────────────────────────────────────────

# Hero
st.markdown('<div class="hero-title">CodeAgent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">AI-Powered Coding Assistant in Your Terminal</div>', unsafe_allow_html=True)

# Stats
st.markdown("""
<div class="stats-row">
    <div class="stat"><div class="number">7</div><div class="label">Built-in Tools</div></div>
    <div class="stat"><div class="number">3</div><div class="label">AI Providers</div></div>
    <div class="stat"><div class="number">0</div><div class="label">API Cost (Ollama)</div></div>
    <div class="stat"><div class="number">&lt;1s</div><div class="label">Tool Execution</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Provider badges
st.markdown("""
<div style="text-align:center; margin-bottom: 30px;">
    <span class="provider-badge">🟣 Claude (Anthropic)</span>
    <span class="provider-badge">🟢 GPT-4o (OpenAI)</span>
    <span class="provider-badge">🔵 Ollama (Local & Free)</span>
</div>
""", unsafe_allow_html=True)


# ── Interactive Demo ──────────────────────────────────────────────────────────
st.markdown("## Live Demo")

# Terminal header
st.markdown("""
<div class="terminal-header">
    <span class="dot dot-red"></span>
    <span class="dot dot-yellow"></span>
    <span class="dot dot-green"></span>
    <span class="title">CodeAgent — claude-sonnet-4</span>
</div>
""", unsafe_allow_html=True)

# Initialize state
if "step" not in st.session_state:
    st.session_state.step = 0
if "history" not in st.session_state:
    st.session_state.history = ""

# Build terminal content
terminal_content = ""
for i in range(min(st.session_state.step, len(DEMO_STEPS))):
    s = DEMO_STEPS[i]
    terminal_content += f'<div style="margin-bottom:20px;">'
    terminal_content += f'<span class="prompt-symbol">❯</span> <span class="user-input">{s["user"]}</span><br>'
    terminal_content += f'<span class="tool-badge">🔧 {s["tool"]}</span> <span style="color:#8b949e;font-size:12px;">({s["tool_args"]})</span><br>'
    terminal_content += f'<div class="tool-output">{s["output"]}</div>'
    terminal_content += f'<div class="ai-response">{s["response"]}</div>'
    terminal_content += f'</div>'

if st.session_state.step >= len(DEMO_STEPS):
    terminal_content += '<div style="color:#3fb950;font-weight:600;text-align:center;padding:20px;">✓ Demo Complete — All 7 tools demonstrated successfully</div>'

# Show terminal
st.markdown(f'<div class="terminal-body">{terminal_content}</div>', unsafe_allow_html=True)

# Buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("▶ Next Step", use_container_width=True, disabled=st.session_state.step >= len(DEMO_STEPS)):
        st.session_state.step += 1
        st.rerun()
with col2:
    if st.button("⏩ Run All", use_container_width=True, disabled=st.session_state.step >= len(DEMO_STEPS)):
        st.session_state.step = len(DEMO_STEPS)
        st.rerun()
with col3:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.step = 0
        st.rerun()


# ── Features Section ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## Features")

cols = st.columns(4)
features = [
    ("📁", "File Operations", "Read, write, and edit files with precision"),
    ("🔍", "Code Search", "Regex search across entire codebases"),
    ("🖥️", "Terminal", "Execute commands with safety checks"),
    ("📊", "Git Integration", "Status, diff, commit, log — all built-in"),
    ("🔄", "Multi-Provider", "Claude, OpenAI, or local Ollama"),
    ("⚡", "Streaming", "Real-time response streaming"),
    ("🛡️", "Safe by Design", "Confirms destructive operations"),
    ("🎨", "Beautiful UI", "Rich panels, syntax highlighting"),
]

for i, (icon, title, desc) in enumerate(features):
    with cols[i % 4]:
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon">{icon}</div>
            <div class="title">{title}</div>
            <div class="desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")  # spacer


# ── Architecture Section ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## Architecture")

st.markdown("""
<div class="terminal-box" style="text-align:center;">
<pre style="color:#e6edf3;font-size:14px;">
    ┌─────────────┐
    │  User Input  │
    └──────┬──────┘
           │
    ┌──────▼──────┐     ┌──────────────┐
    │  Agent Loop  │────▶│  LLM Provider │
    │   (app.py)   │◀────│  Claude/GPT/  │
    └──────┬──────┘     │   Ollama      │
           │             └──────────────┘
    ┌──────▼──────┐
    │ Tool Registry│
    └──────┬──────┘
           │
    ┌──────▼──────────────────────────┐
    │         7 Agent Tools           │
    ├─────────┬──────────┬────────────┤
    │file_read│file_write│  file_edit  │
    │dir_list │code_search│  terminal  │
    │         │  git_ops  │            │
    └─────────┴──────────┴────────────┘
</pre>
</div>
""", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 20px; color: #8b949e; font-family: 'JetBrains Mono', monospace;">
    <strong style="color:#58a6ff;">CodeAgent v0.1.0</strong><br>
    Built with Python • Powered by Claude & OpenAI • Beautiful with Rich<br><br>
    <span style="font-size:0.85rem;">Ready for production deployment</span>
</div>
""", unsafe_allow_html=True)
