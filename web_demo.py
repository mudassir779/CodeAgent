"""CodeAgent - Web Demo for Client Presentations."""

import streamlit as st

st.set_page_config(
    page_title="CodeAgent - AI Coding Assistant",
    page_icon="🤖",
    layout="wide",
)

# ── Minimal CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');

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
.hero-sub {
    text-align: center;
    color: #8b949e;
    font-size: 1.1rem;
    margin-bottom: 30px;
    font-family: 'JetBrains Mono', monospace;
}
.terminal-header {
    background: #1e1e2e;
    border-radius: 12px 12px 0 0;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.terminal-header .dot {
    width: 12px; height: 12px; border-radius: 50%; display: inline-block;
}
.dot-r { background: #ff5f57; }
.dot-y { background: #febc2e; }
.dot-g { background: #28c840; }
.terminal-header .t-title {
    color: #8b949e;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    margin-left: 10px;
}
.terminal-body {
    background: #0d1117;
    border-radius: 0 0 12px 12px;
    padding: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    line-height: 1.7;
    color: #e6edf3;
    min-height: 150px;
}
.user-line { color: #58a6ff; font-weight: 600; }
.prompt-sym { color: #3fb950; font-weight: 700; }
.tool-tag {
    background: #1c2333;
    border: 1px solid #f0883e50;
    border-radius: 6px;
    padding: 2px 8px;
    color: #f0883e;
    font-size: 12px;
}
.tool-out {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    margin: 6px 0 10px 0;
    color: #8b949e;
    font-size: 12px;
    white-space: pre-wrap;
    max-height: 220px;
    overflow-y: auto;
}
.ai-resp { color: #e6edf3; margin: 6px 0 18px 0; }
.ai-resp b { color: #58a6ff; }
.ai-resp em { color: #3fb950; font-style: normal; }
.stat-box {
    text-align: center;
    padding: 20px;
    background: #161b22;
    border-radius: 12px;
    border: 1px solid #30363d;
}
.stat-num {
    font-size: 2rem;
    font-weight: 700;
    color: #58a6ff;
    font-family: 'JetBrains Mono', monospace;
}
.stat-lbl {
    color: #8b949e;
    font-size: 0.85rem;
    font-family: 'JetBrains Mono', monospace;
}
.feat-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    margin-bottom: 12px;
}
.feat-card .f-icon { font-size: 1.8rem; margin-bottom: 8px; }
.feat-card .f-title {
    color: #e6edf3;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 4px;
}
.feat-card .f-desc {
    color: #8b949e;
    font-size: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
}
.provider-tag {
    display: inline-block;
    background: #1c2333;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 6px 14px;
    margin: 4px;
    color: #e6edf3;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)


# ── Demo Steps ────────────────────────────────────────────────────────────────
STEPS = [
    {
        "user": "Read the pyproject.toml file",
        "tool": "file_read",
        "args": "path=pyproject.toml",
        "output": '[build-system]\nrequires = ["setuptools>=68.0", "wheel"]\n\n[project]\nname = "codeagent"\nversion = "0.1.0"\ndescription = "CLI-based AI coding assistant"\nrequires-python = ">=3.10"\ndependencies = [\n    "anthropic>=0.39.0",\n    "openai>=1.50.0",\n    "rich>=13.7.0",\n    "click>=8.1.0",\n]',
        "resp": 'The project uses <b>Python 3.10+</b> with 6 core dependencies: <em>anthropic</em>, <em>openai</em>, <em>rich</em>, <em>click</em>, <em>python-dotenv</em>, and <em>prompt-toolkit</em>.',
    },
    {
        "user": "List the project structure",
        "tool": "directory_list",
        "args": "path=., recursive=true",
        "output": "codeagent/\n  llm/\n    anthropic_provider.py\n    openai_provider.py\n    ollama_provider.py\n    base.py, factory.py, types.py\n  tools/\n    file_read.py, file_write.py\n    file_edit.py, directory_list.py\n    code_search.py, terminal.py\n    git_ops.py, registry.py\n  ui/\n    console.py, panels.py, spinner.py\n  app.py, cli.py, config.py",
        "resp": 'Clean <b>modular architecture</b>: <em>llm/</em> for AI providers, <em>tools/</em> for 7 agent tools, <em>ui/</em> for Rich terminal components.',
    },
    {
        "user": "Search for 'def execute' in tools",
        "tool": "code_search",
        "args": "pattern=def execute, path=codeagent/tools",
        "output": "Found 7 matches:\n\nfile_read.py:35      def execute(self, path, offset, limit)\nfile_write.py:31     def execute(self, path, content)\nfile_edit.py:40      def execute(self, path, old_string, new_string)\ndirectory_list.py:31 def execute(self, path, recursive)\ncode_search.py:48    def execute(self, pattern, path, glob)\nterminal.py:35       def execute(self, command, timeout)\ngit_ops.py:35        def execute(self, operation, args)",
        "resp": 'All <b>7 tools</b> implement the same <em>BaseTool</em> interface. The LLM decides which tool to call based on user request.',
    },
    {
        "user": "Create a fibonacci.py file",
        "tool": "file_write",
        "args": "path=fibonacci.py",
        "output": "Written 18 lines to fibonacci.py",
        "resp": 'Created <b>fibonacci.py</b> with type-annotated functions, docstrings, and a main block. Production-quality code.',
    },
    {
        "user": "Run the fibonacci file",
        "tool": "terminal",
        "args": "command=python3 fibonacci.py",
        "output": "Exit code: 0\nFibonacci sequence (first 10):\n[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]\n\nThe 20th Fibonacci number is: 6765",
        "resp": 'CodeAgent can <b>write code</b>, <b>run it immediately</b>, and <b>debug</b> if anything fails. All in one conversation.',
    },
    {
        "user": "Show git status",
        "tool": "git_ops",
        "args": "operation=status",
        "output": "On branch main\nChanges to be committed:\n  new file:   fibonacci.py\n\nUntracked files:\n  web_demo.py",
        "resp": 'Git integration built-in. I can run <b>status</b>, <b>diff</b>, <b>add</b>, <b>commit</b>, and <b>log</b> through natural language.',
    },
]

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">CodeAgent</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">AI-Powered Coding Assistant in Your Terminal</div>', unsafe_allow_html=True)

# Stats row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat-box"><div class="stat-num">7</div><div class="stat-lbl">Built-in Tools</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-box"><div class="stat-num">3</div><div class="stat-lbl">AI Providers</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat-box"><div class="stat-num">$0</div><div class="stat-lbl">Ollama Cost</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="stat-box"><div class="stat-num">&lt;1s</div><div class="stat-lbl">Tool Execution</div></div>', unsafe_allow_html=True)

st.markdown("")

# Provider badges
st.markdown(
    '<div style="text-align:center;margin:10px 0 20px;">'
    '<span class="provider-tag">Claude (Anthropic)</span>'
    '<span class="provider-tag">GPT-4o (OpenAI)</span>'
    '<span class="provider-tag">Ollama (Local & Free)</span>'
    '</div>',
    unsafe_allow_html=True,
)

st.divider()

# ── Live Demo ─────────────────────────────────────────────────────────────────
st.markdown("### Live Demo")

# Terminal chrome
st.markdown(
    '<div class="terminal-header">'
    '<span class="dot dot-r"></span>'
    '<span class="dot dot-y"></span>'
    '<span class="dot dot-g"></span>'
    '<span class="t-title">CodeAgent &mdash; claude-sonnet-4</span>'
    '</div>',
    unsafe_allow_html=True,
)

# Session state
if "step" not in st.session_state:
    st.session_state.step = 0

# Build terminal HTML
html = ""
for i in range(min(st.session_state.step, len(STEPS))):
    s = STEPS[i]
    html += f'<div style="margin-bottom:16px;">'
    html += f'<span class="prompt-sym">&#10095;</span> <span class="user-line">{s["user"]}</span><br>'
    html += f'<span class="tool-tag">&#128295; {s["tool"]}</span> <span style="color:#8b949e;font-size:11px;">({s["args"]})</span>'
    html += f'<div class="tool-out">{s["output"]}</div>'
    html += f'<div class="ai-resp">{s["resp"]}</div>'
    html += f'</div>'

if st.session_state.step >= len(STEPS):
    html += '<div style="color:#3fb950;font-weight:600;text-align:center;padding:16px;">&#10003; Demo Complete &mdash; All tools demonstrated successfully</div>'

if st.session_state.step == 0:
    html += '<div style="color:#8b949e;text-align:center;padding:30px;">Click <b>Next Step</b> to start the demo</div>'

st.markdown(f'<div class="terminal-body">{html}</div>', unsafe_allow_html=True)

# Buttons
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("Next Step ▶", use_container_width=True, disabled=st.session_state.step >= len(STEPS)):
        st.session_state.step += 1
        st.rerun()
with b2:
    if st.button("Run All ⏩", use_container_width=True, disabled=st.session_state.step >= len(STEPS)):
        st.session_state.step = len(STEPS)
        st.rerun()
with b3:
    if st.button("Reset 🔄", use_container_width=True):
        st.session_state.step = 0
        st.rerun()

st.divider()

# ── Features ──────────────────────────────────────────────────────────────────
st.markdown("### Features")

features = [
    ("📁", "File Operations", "Read, write, edit files"),
    ("🔍", "Code Search", "Regex search across codebases"),
    ("🖥️", "Terminal", "Execute commands safely"),
    ("📊", "Git Integration", "Status, diff, commit, log"),
]
features2 = [
    ("🔄", "Multi-Provider", "Claude, OpenAI, Ollama"),
    ("⚡", "Streaming", "Real-time response output"),
    ("🛡️", "Safe by Design", "Confirms destructive ops"),
    ("🎨", "Beautiful UI", "Rich panels & highlighting"),
]

cols = st.columns(4)
for i, (icon, title, desc) in enumerate(features):
    with cols[i]:
        st.markdown(
            f'<div class="feat-card">'
            f'<div class="f-icon">{icon}</div>'
            f'<div class="f-title">{title}</div>'
            f'<div class="f-desc">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

cols2 = st.columns(4)
for i, (icon, title, desc) in enumerate(features2):
    with cols2[i]:
        st.markdown(
            f'<div class="feat-card">'
            f'<div class="f-icon">{icon}</div>'
            f'<div class="f-title">{title}</div>'
            f'<div class="f-desc">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.divider()

# ── Architecture ──────────────────────────────────────────────────────────────
st.markdown("### Architecture")

st.code("""
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
    │dir_list │code_srch │  terminal  │
    │         │  git_ops │            │
    └─────────┴──────────┴────────────┘
""", language=None)

# Footer
st.divider()
st.markdown(
    '<div style="text-align:center;padding:10px;color:#8b949e;font-family:JetBrains Mono,monospace;">'
    '<b style="color:#58a6ff;">CodeAgent v0.1.0</b><br>'
    'Built with Python &bull; Powered by Claude &amp; OpenAI &bull; Beautiful with Rich'
    '</div>',
    unsafe_allow_html=True,
)
