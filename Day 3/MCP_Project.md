# Building Your First MCP Chatbot

You are about to build a chatbot that can **read your own files** and answer questions about them — using a local AI model, running completely offline on your machine.

A normal chatbot only knows what it was trained on:

```text
You → "What was my app idea?"
AI  → "I don't know. I can't access your files."
```

Your chatbot will actually open the file and read it:

```text
You → "What was my app idea?"
AI  → [calls list_available_notes]
AI  → [calls read_note_content("app_idea.txt")]
AI  → "Your app idea is PocketProfessor — a mobile app that lets
        students chat with any textbook PDF, works fully offline."
```

This is powered by **MCP** — and by the end of this guide you will understand every line of code that makes it work.

---

## What Is MCP? (The Simple Explanation)

**MCP** stands for **Model Context Protocol**.

The word "protocol" just means a **standard agreement** about how two things talk to each other. HTTP is a protocol for web browsers and servers. MCP is a protocol for AI models and tools.

**The USB-C analogy:**

> USB-C is a standard connector. You can plug any USB-C device (phone, laptop, monitor) into any USB-C charger — the devices don't have to know anything specific about each other.

MCP is the same idea for AI:
*   Any AI app (Cursor, Claude Desktop, your Python script) can plug into any MCP tool.
*   The tool doesn't care which AI is calling it.
*   The AI doesn't care how the tool is built.

| Without MCP | With MCP |
| :--- | :--- |
| You write Slack integration for ChatGPT | You write one Slack MCP server |
| Then rewrite it for Claude | Claude connects to the same server |
| Then rewrite it again for your local LLM | Your local LLM connects too |
| 3× work, 3× bugs | 1× work, works everywhere |

**In this project:**
*   `mcp_tool.py` is the **MCP server** — it exposes your notes folder as two tools.
*   `ollama_client.py` is the **MCP client** — it runs the chatbot and connects to the server.

---

## The Two Files You Need to Understand

```text
mcp_project/
│
├── mcp_tool.py        ← THE SERVER  (your tools live here)
│                        Notes tools  : list_available_notes, read_note_content
│                        To-do tools  : add_todo, list_todos, complete_todo, delete_todo
│
├── ollama_client.py   ← THE CLIENT  (the chatbot lives here)
│                        Starts the server, talks to the LLM, runs tools
│
└── my_notes/          ← Your files (notes + to-do list)
    ├── app_idea.txt
    ├── meeting_notes.txt
    ├── todo.json       ← auto-created when you add your first task
    └── ...
```

The server and client run as **two separate Python processes**. The client starts the server automatically — you only ever run `python ollama_client.py`.

---

## How It All Works: The Big Picture

```text
  YOU type a question
        │
        ▼
  ollama_client.py
        │
        │  1. "Here's the question + here are your available tools"
        ▼
  Ollama LLM (llama3.2 running locally)
        │
        │  2. "I need to call list_available_notes"
        ▼
  ollama_client.py receives tool_call request
        │
        │  3. Sends request over a pipe
        ▼
  mcp_tool.py (running as a subprocess)
        │
        │  4. Runs the Python function, returns result
        ▼
  ollama_client.py receives result
        │
        │  5. "Here's what the tool returned, now answer"
        ▼
  Ollama LLM
        │
        │  6. Produces a final answer
        ▼
  YOU see the answer
```

The key insight: **the LLM never runs your Python code**. It only *asks* for tools to be called. The client (your Python code) does the actual running and feeds the result back.

---

## All Available Tools

| Tool | Group | What it does |
| :--- | :--- | :--- |
| `list_available_notes` | Notes | Lists all `.txt` files in `my_notes/` |
| `read_note_content(filename)` | Notes | Reads and returns the full text of a note |
| `add_todo(task)` | To-Do | Creates a new task, saves it with ID + timestamp |
| `list_todos(filter)` | To-Do | Shows tasks — `"all"`, `"pending"`, or `"done"` |
| `complete_todo(task_id)` | To-Do | Marks a task done, records exact date & time |
| `delete_todo(task_id)` | To-Do | Permanently removes a task by ID |

The AI will call these **automatically** based on what you say:

| You say | AI does |
| :--- | :--- |
| *"I need to fix the login bug"* | calls `add_todo("Fix the login bug")` |
| *"I finished the design review"* | calls `complete_todo(matching_id)` |
| *"What do I still need to do?"* | calls `list_todos("pending")` |
| *"Remove task 3"* | calls `delete_todo(3)` |
| *"What was my app idea?"* | calls `list_available_notes`, then `read_note_content` |

---

## Part 1 — The MCP Server (`mcp_tool.py`)

### Why do we even need a "server"?

Good question. The AI model (Ollama) runs in its own process. Your tools (reading files) run in a Python process. These are different programs — they can't share memory or call each other's functions directly.

A **server** is just a program that sits and waits for requests, handles them, and sends back responses. Here, the server is tiny — it's just your two Python functions wrapped so the AI can reach them.

Think of it like this:
> Your functions are the **kitchen**. The MCP server is the **waiter window** between the kitchen and the dining room (the AI).

### Full annotated code

```python
import os
from mcp.server.fastmcp import FastMCP

# FastMCP handles all the behind-the-scenes work:
# receiving requests, calling your functions, sending results.
# "SmartReferenceDesk" = the name of this server (shown in Cursor UI, Claude UI etc.)
mcp = FastMCP("SmartReferenceDesk")

NOTES_FOLDER = "./my_notes"
os.makedirs(NOTES_FOLDER, exist_ok=True)  # auto-create folder on first run
```

### The `@mcp.tool()` decorator — the most important line

A **decorator** is a function that wraps another function and adds behaviour. You've probably seen `@staticmethod` or `@property`. `@mcp.tool()` tells FastMCP: *"expose this function as a tool the AI can call."*

When you add `@mcp.tool()`, three things get automatically read:

```python
@mcp.tool()
def read_note_content(filename: str) -> str:
    """Reads and returns the exact text content of a specified note file."""
    ...
```

| What FastMCP reads | What it becomes |
| :--- | :--- |
| Function name: `read_note_content` | Tool ID the AI uses to call it |
| Docstring | The description the AI reads to decide **when** to use this tool |
| Type hint `filename: str` | A JSON Schema: `{"type": "string"}` so the AI knows what to pass |

The generated tool card looks like this:
```json
{
  "name": "read_note_content",
  "description": "Reads and returns the exact text content of a specified note file.",
  "parameters": {
    "type": "object",
    "properties": { "filename": { "type": "string" } },
    "required": ["filename"]
  }
}
```

The AI receives this card. When you ask *"what was my app idea?"*, the AI reads the description and thinks: *"read_note_content sounds right for this"*.

### Why good docstrings matter (critical)

The docstring is the **only thing the LLM reads** to decide whether to call your tool.

```python
# Bad docstring → AI will ignore or misuse this tool
def read_note_content(filename: str) -> str:
    """Reads a file."""
    ...

# Good docstring → AI knows exactly when and how to use this
def read_note_content(filename: str) -> str:
    """Reads and returns the exact text content of a specified note file."""
    ...
```

This is true in production too. GitHub's MCP server, Slack's MCP server — they all succeed or fail based on the quality of their tool descriptions.

### The To-Do Manager tools

The to-do list is stored as a JSON file at `my_notes/todo.json`. Each task looks like this:

```json
{
  "id": 1,
  "task": "Fix the login bug",
  "status": "pending",
  "created_at": "2026-05-25 01:00:00",
  "completed_at": null
}
```

When you call `complete_todo(1)`, the status flips to `"done"` and `completed_at` gets the real timestamp:

```json
{
  "id": 1,
  "task": "Fix the login bug",
  "status": "done",
  "created_at": "2026-05-25 01:00:00",
  "completed_at": "2026-05-25 14:32:07"
}
```

The file is updated on every `add_todo`, `complete_todo`, and `delete_todo` call, so your task list survives restarts.

**Why JSON and not a .txt file?**
Because JSON gives us structure — each task has an ID, status, and two timestamps. A plain text file would make it hard to find and update a specific task.

---

### Transport: how the server communicates

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

`transport="stdio"` means the server reads requests from **stdin** (standard input) and writes responses to **stdout** (standard output).

```text
ollama_client.py  ──writes to──►  mcp_tool.py's stdin   (sends requests)
ollama_client.py  ◄──reads from── mcp_tool.py's stdout  (receives results)
```

This is the simplest possible communication channel — the same pipes that connect commands in a terminal (`cat file.txt | grep hello`). No network, no ports, no firewall rules.

---

## Part 2 — The Chatbot Client (`ollama_client.py`)

### What is `async` / `await`? (Plain English)

You will notice every important function starts with `async` and uses `await`. Here is why.

Imagine you order food at a restaurant. You have two choices:
1. **Blocking (bad):** Stand at the counter, stare at the chef, don't move until your food arrives.
2. **Non-blocking (async, good):** Give your order, sit down, do other things, get notified when food is ready.

Our program talks to two external processes — Ollama (the LLM) and the MCP server (via pipes). Both can take a moment to respond. If we used blocking code, the entire program would freeze while waiting.

`async/await` tells Python: *"while I'm waiting for this, go do other things."*

```python
# This pauses here and lets Python do other work while waiting
result = await agent.ainvoke({"messages": history})
```

You don't need to master `asyncio` to use this code. Just know: if you see `await`, it means "wait for this but don't block everything else".

### What is LangChain and why use it here?

**LangChain** is a Python library that makes it easier to build LLM-powered apps. Without it, connecting an MCP server to Ollama requires writing a lot of boilerplate code.

**Before LangChain** (manual version):
```python
# Had to do all of this by hand:
mcp_tools = (await session.list_tools()).tools
ollama_tools = [
    {
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description,
            "parameters": t.inputSchema,
        },
    }
    for t in mcp_tools
]
# ...then manually handle tool_calls...
# ...then manually loop back to the LLM...
```

**After LangChain** (what we use):
```python
tools = await load_mcp_tools(session)   # discovers + converts all MCP tools
agent = create_react_agent(llm, tools)  # builds the full LLM ↔ tool loop
```

Two lines replace forty. That's why LangChain is useful.

### What is `create_react_agent`?

The name comes from a technique called **ReAct** (Reason + Act), described in a 2022 research paper. It is the engine behind almost every tool-using AI agent today.

The loop it runs:

```text
Step 1 — REASON:  LLM gets your question + the list of tools.
                  It thinks: "Should I call a tool? Which one? With what args?"

Step 2 — ACT:     LLM emits a tool_call (or a final answer if no tool needed).

Step 3 — OBSERVE: We run the tool. Result goes back to the LLM as a new message.

Step 4 — REPEAT:  Back to Step 1, now with more context.
                  LLM either calls another tool or gives the final answer.
```

Example for the question *"What bugs are open?"*:

```text
[REASON] I should look at the notes. Let me list them first.
[ACT]    tool_call: list_available_notes()
[OBSERVE] Available notes: bug_log.txt, app_idea.txt, ...
[REASON] bug_log.txt looks relevant. Let me read it.
[ACT]    tool_call: read_note_content(filename="bug_log.txt")
[OBSERVE] Content: 3 open bugs — retrieval regression, memory leak...
[REASON] I have enough information. No more tool calls needed.
[ACT]    Final answer: "You have 3 open bugs: ..."
```

All of this happens automatically inside `create_react_agent`. You just call `agent.ainvoke({"messages": history})` and get back the final answer.

### What is the system prompt?

```python
SYSTEM_PROMPT = (
    "You are a helpful assistant with access to the user's personal notes "
    "via MCP tools. Use list_available_notes to see what files exist, then "
    "read_note_content to read any you need. Answer concisely."
)
```

The system prompt is a hidden instruction given to the AI at the start of every conversation. The user never sees it. Think of it as the AI's job description.

Without a good system prompt, a small local model like `llama3.2` might forget to use tools at all and try to answer from memory. The system prompt reminds it: *"you have tools — use them."*

### Conversation history: why we keep it

```python
history = [SystemMessage(content=SYSTEM_PROMPT)]  # starts here

# After first question:
# history = [SystemMessage, HumanMessage("what notes?"), AIMessage("..."), ToolMessage("..."), AIMessage("You have 10 notes")]

# After second question:
# history = [...everything above..., HumanMessage("now read app_idea"), ...]
```

By keeping the full history, follow-up questions work naturally:

```text
You: what notes do I have?
AI:  You have 10 notes: app_idea, meeting_notes, ...

You: read the app idea one    ← follow-up works because AI remembers the list
AI:  Your app idea is PocketProfessor...
```

If we cleared history between questions, the second question would fail because the AI would have forgotten its tool results.

---

## How To Run This Project

### What you need before starting

| Requirement | Check command | Install link |
| :--- | :--- | :--- |
| Python 3.10+ | `python --version` | [python.org](https://python.org) |
| Ollama | `ollama --version` | [ollama.com](https://ollama.com) |
| llama3.2 model | `ollama list` | see step 2 below |

### Step 1 — Install the Python packages

```bash
pip install mcp langchain-ollama langchain-mcp-adapters langgraph
```

What each package does:

| Package | Job |
| :--- | :--- |
| `mcp` | The MCP protocol SDK — runs the server, handles the pipes |
| `langchain-ollama` | Connects LangChain to your local Ollama LLM |
| `langchain-mcp-adapters` | One-line conversion from MCP tools → LangChain tools |
| `langgraph` | Provides `create_react_agent` — the ReAct loop engine |

### Step 2 — Start Ollama and download the model

```bash
# Download the model (only needed once, ~2GB)
ollama pull llama3.2

# Check it downloaded
ollama list

# Make sure Ollama is running (open the Ollama app, or run this)
ollama serve
```

### Step 3 — Run the chatbot

```bash
cd day5_mcp_and_automation/mcp_project
python ollama_client.py
```

### What you will see

```text
Starting MCP server...
Tools: ['list_available_notes', 'read_note_content', 'add_todo',
        'list_todos', 'complete_todo', 'delete_todo']
Type 'exit' to quit, 'clear' to reset history.

You: I need to benchmark Qdrant vs FAISS this week

AI: Got it! I've added that to your to-do list.
    ⬜ [1] Benchmark Qdrant vs FAISS this week
       Added : 2026-05-25 01:15:32

You: also remind me to write the migration RFC

AI: Added!
    ⬜ [2] Write the migration RFC
       Added : 2026-05-25 01:15:48

You: what do I still need to do?

AI: ⬜ Pending Tasks

    ⬜ [1] Benchmark Qdrant vs FAISS this week
         Added : 2026-05-25 01:15:32

    ⬜ [2] Write the migration RFC
         Added : 2026-05-25 01:15:48

You: I finished the benchmarking

AI: Great work! Marking it done.
    ✅ Task marked as done!
       ID        : 1
       Task      : Benchmark Qdrant vs FAISS this week
       Completed : 2026-05-25 14:30:05

You: what was the app idea in my notes?

AI: Your app idea is "PocketProfessor" — a mobile app that lets
students chat with any textbook PDF and works fully offline.

You: exit
Goodbye!
```

### Chatbot commands

| Type this | What happens |
| :--- | :--- |
| any question | AI answers, using tools if needed |
| `exit` / `quit` / `:q` | Leaves the chatbot cleanly |
| `clear` | Wipes conversation history — fresh start |
| `Ctrl+C` at the prompt | Exits immediately |
| `Ctrl+C` mid-answer | Cancels that turn, keeps chatting |

### Step 4 — Add your own notes

Drop any `.txt` file into `my_notes/` and ask about it right away — no restart needed:

```bash
echo "Team meeting every Monday at 10:30 AM" > my_notes/schedule.txt
```

Then in the chatbot:
```text
You: when is the team meeting?
```

---

## Connect This Server to Desktop AI Apps

The same `mcp_tool.py` works with Cursor, Claude Desktop, and any other MCP-compatible app **without changing a single line**. That is the point of the standard.

> **Before you start:** find the absolute path to your `mcp_tool.py` file.
> On macOS/Linux, run `pwd` from inside the `mcp_project` folder and append `/mcp_tool.py`.
> Example: `/Users/yourname/projects/gen-ai-notebook/day5_mcp_and_automation/mcp_project/mcp_tool.py`

---

### Cursor

Cursor stores MCP server configs in a JSON file.

**Step 1 — Create or open the config**

*   Recommended (project-level): create `.cursor/mcp.json` inside your repo root.
*   Alternative (global): `~/.cursor/mcp.json`

**Step 2 — Add this JSON**

```json
{
  "mcpServers": {
    "smart-reference-desk": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp_project/mcp_tool.py"]
    }
  }
}
```

**Step 3 — Restart Cursor**

Go to Settings → MCP. You should see `smart-reference-desk` with a green dot and two tools listed.

**Step 4 — Use it**

In the Cursor chat, ask:
```text
What notes do I have? Read app_idea.txt and summarize it.
```

Cursor's AI will call your tools automatically.

---

### Claude Desktop

Claude Desktop is the app that originally shipped MCP support.

**Step 1 — Find the config file**

| Your OS | Config file location |
| :--- | :--- |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Step 2 — Add this JSON** (create the file if it doesn't exist)

```json
{
  "mcpServers": {
    "smart-reference-desk": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/mcp_project/mcp_tool.py"]
    }
  }
}
```

**Step 3 — Quit and reopen Claude Desktop**

In the chat input box you should see a hammer icon (🔨). Click it — it should list your 2 tools.

**Step 4 — Use it**

```text
List my notes and then summarize the Japan travel plan.
```

---

### Antigravity (Google's Agentic IDE)

**Step 1** — Open Antigravity → Settings → Agents → MCP Servers.

**Step 2** — Click **Add Server** and fill in the form (or paste JSON):

```json
{
  "name": "smart-reference-desk",
  "command": "python",
  "args": ["/ABSOLUTE/PATH/TO/mcp_project/mcp_tool.py"]
}
```

**Step 3** — Save. Antigravity will spawn the server.

> **Tip:** If the server is not detected, use the absolute path to your virtual environment's Python binary instead of just `"python"`. For example: `/Users/yourname/.venv/bin/python`.

---

### Any other MCP-compatible app

Most clients (Continue, Zed, VS Code Copilot extensions) follow the same pattern:

```json
{
  "command": "python",
  "args": ["/ABSOLUTE/PATH/TO/mcp_project/mcp_tool.py"],
  "transport": "stdio"
}
```

If the app says it supports MCP, this is all you need.

---

## Every Beginner Question, Answered

**Q: Is the LLM running my Python code?**

No. The LLM only *proposes* which tool to call and with what arguments. The actual Python function is always run by the MCP server (your own process). The LLM never has direct access to your file system.

---

**Q: Why `async/await` everywhere?**

Because the program talks to two external processes (Ollama and the MCP server) and needs to wait for both without freezing. `async/await` lets Python handle the waiting efficiently. If you see `await`, it just means "wait here, but don't block other things."

---

**Q: What is the difference between MCP and just calling a function directly?**

When you write `read_note_content()` directly in Python, only your Python script can call it. With MCP:
*   Cursor can call it.
*   Claude Desktop can call it.
*   Your Python script can call it.
*   Any future MCP client can call it.

MCP makes your tool reusable by anything that speaks the protocol.

---

**Q: What is the difference between MCP and OpenAI function calling?**

Function calling is a feature built into specific LLMs (GPT-4, Gemini, etc.) — the format is different for each provider. MCP is a **transport-level standard** that sits on top of tool calling: it defines how the tool *server* is started, how the tool *list* is discovered, and how *results* are sent back — in a way that works across all LLMs and all clients.

In this project:
*   `ChatOllama` does the LLM-level tool calling (Ollama's format).
*   `langchain-mcp-adapters` is the bridge that wraps MCP tools into LangChain's tool format.
*   MCP handles the server ↔ client communication over stdio.

---

**Q: What is LangGraph and how is it different from LangChain?**

LangChain is a toolkit of building blocks (LLMs, tools, prompts, chains). LangGraph is a newer layer built on top of LangChain that lets you define **stateful graphs** — loops and branches where LLMs, tools, and humans can interact. `create_react_agent` is a pre-built LangGraph graph that implements the ReAct loop for you.

---

**Q: What is ReAct?**

ReAct = **Re**ason + **Act**. It is a pattern published in a 2022 research paper that became the foundation for almost all tool-using AI agents. The idea: let the LLM alternate between writing its reasoning ("I should look at the notes") and taking actions (calling a tool). This is more reliable than just prompting an LLM and hoping it calls the right tool.

---

**Q: Does the LLM always use a tool?**

No. If the question can be answered from context already in the conversation, the LLM will answer directly without calling any tool. For example:

```text
You: what notes do I have?
AI:  [calls list_available_notes]  ← tool call needed
AI:  You have 10 notes.

You: how many is that?
AI:  That's 10 notes.              ← no tool call, already knows
```

---

**Q: Do I need internet access?**

No. Everything runs locally:
*   Ollama runs the LLM on your machine.
*   The MCP server reads files from your machine.
*   No data leaves your computer.

---

**Q: Can I add more tools?**

Yes — just add another function with `@mcp.tool()` to `mcp_tool.py`. No changes needed to `ollama_client.py`. The client discovers tools automatically at startup.

```python
@mcp.tool()
def count_words_in_note(filename: str) -> str:
    """Counts and returns the number of words in a specified note file."""
    filepath = os.path.join(NOTES_FOLDER, filename)
    with open(filepath, 'r') as f:
        return f"Word count: {len(f.read().split())}"
```

---

**Q: Can a tool call another tool?**

Not directly. The LLM is always the orchestrator. A tool runs a Python function and returns a plain text result. The LLM then decides whether to call another tool based on what it got back.

---

**Q: Why does the notes folder need `.txt` files only?**

That is a deliberate simplification for this beginner project. In production you would add tools for reading `.pdf`, `.md`, querying databases, calling REST APIs, etc. The pattern is always the same: write a Python function, add `@mcp.tool()`, give it a clear docstring.

---

## Troubleshooting

| Problem | Most likely cause | How to fix |
| :--- | :--- | :--- |
| `ModuleNotFoundError` | Packages not installed | Run `pip install mcp langchain-ollama langchain-mcp-adapters langgraph` |
| Server closes immediately | `mcp_tool.py` has a Python error | Run `python mcp_tool.py` directly and read the error |
| `connection refused` / Ollama error | Ollama is not running | Open the Ollama app or run `ollama serve` in a terminal |
| LLM gives answer without using tools | Wrong model (not tool-capable) | Use `llama3.2`, `qwen2.5`, or `mistral-nemo` |
| LLM gives answer without using tools | Question too vague | Add context: *"Look at my notes and tell me..."* |
| Tools list is empty in Cursor/Claude | Relative path in config | Use the **full absolute path** to `mcp_tool.py` |
| `pydantic` errors | Old LangChain packages | Run `pip install -U langchain-core langgraph` |

---

## Where This Is Used in Real Companies

This exact same pattern — **expose tools via MCP, connect any LLM, use LangGraph for orchestration** — powers production systems:

| Use case | MCP tools involved |
| :--- | :--- |
| IDE agents (Cursor, Zed) | Read files, run tests, search codebase, open PRs |
| Internal knowledge bots | Slack messages, Notion pages, Google Drive docs |
| Data analytics agents | Postgres queries, Snowflake tables, CSV files |
| Customer support automation | Zendesk tickets, Stripe refunds, order status APIs |
| Personal AI assistants | Calendar, email, file system, browser |

The only difference between this project and those is the number of tools.

---

## Real Industry Architecture

```text
  User (Slack / Web UI / IDE)
          │
          ▼
  Agent Orchestrator (LangGraph)
          │
          ├── LLM (Claude / GPT-4o / llama3.2 via Ollama)
          │
          └── MCP Servers
               ├── GitHub MCP      → read issues, open PRs
               ├── Postgres MCP    → query databases
               ├── Slack MCP       → post messages
               ├── Filesystem MCP  → read/write local files   ← you built this
               └── Custom MCP      → your own tools
```

| Layer | Technologies |
| :--- | :--- |
| **MCP Servers** | FastMCP, official SDKs (TypeScript, Python, Go) |
| **MCP Clients** | Cursor, Claude Desktop, Antigravity, Continue, Zed |
| **LLMs** | Claude, GPT-4o, Llama 3, Mistral, Qwen |
| **Orchestration** | LangGraph, CrewAI, AutoGen |
| **Transport** | stdio (local), SSE / HTTP (remote) |

---

## Common Production Mistakes

1. **Vague tool descriptions** → the LLM picks the wrong tool. Always write a clear, specific docstring.
2. **Too many tools** → the LLM gets confused about which one to use. Group related tools into separate servers.
3. **No error handling in tools** → one bad file crashes the whole session. Always wrap tool functions in `try/except`.
4. **Blocking code in async tools** → freezes the event loop. Use `asyncio.to_thread()` for any blocking I/O.
5. **No auth on remote servers** → anyone on the internet can call your tools. Add authentication before exposing any MCP server publicly.

---

## What You Just Built

Two files. ~130 lines of Python. A complete working AI agent:

```text
mcp_tool.py  (~90 lines with comments)
  └── Exposes 2 tools via MCP over stdio

ollama_client.py  (~120 lines with comments)
  └── Starts the MCP server automatically
  └── Discovers tools with load_mcp_tools()
  └── Creates a ReAct agent with create_react_agent()
  └── Runs an infinite, multi-turn chat loop
  └── Preserves full conversation history
  └── Works with exit, clear, Ctrl+C
```

This is the same architectural pattern used in every modern AI IDE and agent platform. The only difference is scale — more tools, bigger models, remote transport instead of stdio.

**Next steps to go deeper:**
*   Add a `search_notes(query: str)` tool that does keyword search across all files.
*   Add a `write_note(filename: str, content: str)` tool so the AI can save new notes.
*   Replace the local notes folder with a real database or API.
*   Add a second MCP server (e.g. weather, calculator) and let the agent use tools from both.
