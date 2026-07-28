import json
import os
from datetime import datetime

from mcp.server.fastmcp import FastMCP

# ============================================================
# WHAT IS THIS FILE?
#
# This is the MCP Server — it exposes tools the AI can call.
# Two groups of tools live here:
#
#   GROUP 1 — Notes Reader (read-only)
#     • list_available_notes   → see what .txt files exist
#     • read_note_content      → read a specific file
#
#   GROUP 2 — To-Do Manager (read + write)
#     • add_todo       → create a new task
#     • list_todos     → see all / pending / done tasks
#     • complete_todo  → mark a task done (stamps date & time)
#     • delete_todo    → permanently remove a task
#
# All to-dos are persisted in:  my_notes/todo.json
# ============================================================


mcp = FastMCP("SmartReferenceDesk")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Creates my_notes beside mcp_tool.py
NOTES_FOLDER = os.path.join(BASE_DIR, "my_notes")

TODO_FILE = os.path.join(NOTES_FOLDER, "todo.json")


os.makedirs(NOTES_FOLDER, exist_ok=True)


# ── Helpers ───────────────────────────────────────────────────
# These are plain functions, NOT tools (no @mcp.tool decorator).
# They are only used internally by the tools below.

def _load_todos() -> list:
    """Read the todo.json file and return a list of task dicts."""
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)


def _save_todos(todos: list) -> None:
    """Write the list of task dicts back to todo.json."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def _next_id(todos: list) -> int:
    """Return the next available integer ID."""
    return max((t["id"] for t in todos), default=0) + 1


def _format_todo(todo: dict) -> str:
    """Format a single task as a readable string."""
    status_icon = "✅" if todo["status"] == "done" else "⬜"
    line = f'{status_icon} [{todo["id"]}] {todo["task"]}'
    line += f'\n     Added : {todo["created_at"]}'
    if todo["status"] == "done":
        line += f'\n     Done  : {todo["completed_at"]}'
    return line


# ═════════════════════════════════════════════════════════════
# GROUP 1 — Notes Reader Tools (read-only)
# ═════════════════════════════════════════════════════════════

@mcp.tool()
def list_available_notes() -> str:
    """Returns a list of all text files currently in the notes folder."""
    try:
        files = [f for f in os.listdir(NOTES_FOLDER) if f.endswith(".txt")]
        if not files:
            return "No text files found."
        return f"Available notes: {', '.join(files)}"
    except Exception as e:
        return f"Error reading folder: {str(e)}"


@mcp.tool()
def read_note_content(filename: str) -> str:
    """Reads and returns the exact text content of a specified note file."""
    if not filename.endswith(".txt"):
        return "Error: Can only read .txt files."

    filepath = os.path.join(NOTES_FOLDER, filename)
    try:
        with open(filepath, "r") as file:
            return f"--- Content of {filename} ---\n{file.read()}"
    except FileNotFoundError:
        return f"Error: Note '{filename}' does not exist."


# ═════════════════════════════════════════════════════════════
# GROUP 2 — To-Do Manager Tools
# ═════════════════════════════════════════════════════════════

@mcp.tool()
def add_todo(task: str) -> str:
    """
    Adds a new to-do task to the task list and saves it.
    Use this whenever the user mentions something they need to do, a task,
    a reminder, an action item, or any work that should be tracked.
    Returns the new task with its assigned ID.
    """
    todos = _load_todos()

    new_task = {
        "id": _next_id(todos),
        "task": task.strip(),
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None,
    }

    todos.append(new_task)
    _save_todos(todos)

    return (
        f"✅ Task added!\n"
        f"   ID     : {new_task['id']}\n"
        f"   Task   : {new_task['task']}\n"
        f"   Added  : {new_task['created_at']}"
    )


@mcp.tool()
def list_todos(filter: str = "all") -> str:
    """
    Returns the current to-do list. The filter parameter controls what is shown:
      'all'     → every task (default)
      'pending' → only tasks not yet completed
      'done'    → only completed tasks
    Use this when the user asks about their tasks, what's left to do,
    what they've completed, or wants a summary of their to-do list.
    """
    todos = _load_todos()

    if filter == "pending":
        todos = [t for t in todos if t["status"] == "pending"]
        heading = "⬜ Pending Tasks"
    elif filter == "done":
        todos = [t for t in todos if t["status"] == "done"]
        heading = "✅ Completed Tasks"
    else:
        heading = "📋 All Tasks"

    if not todos:
        return f"{heading}\n\nNo tasks found."

    lines = [heading, ""]
    for todo in todos:
        lines.append(_format_todo(todo))
        lines.append("")

    return "\n".join(lines).strip()


@mcp.tool()
def complete_todo(task_id: int) -> str:
    """
    Marks a to-do task as completed and records the exact date and time it was finished.
    Use this when the user says they finished a task, completed something,
    or says something like 'done', 'mark X as done', or 'I finished task N'.
    The task_id must be the integer ID shown in list_todos.
    """
    todos = _load_todos()

    for todo in todos:
        if todo["id"] == task_id:
            if todo["status"] == "done":
                return f"Task [{task_id}] is already marked as done (completed: {todo['completed_at']})."

            todo["status"] = "done"
            todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            _save_todos(todos)

            return (
                f"✅ Task marked as done!\n"
                f"   ID        : {todo['id']}\n"
                f"   Task      : {todo['task']}\n"
                f"   Completed : {todo['completed_at']}"
            )

    return f"Error: No task found with ID {task_id}. Use list_todos to see valid IDs."


@mcp.tool()
def delete_todo(task_id: int) -> str:
    """
    Permanently removes a task from the to-do list by its ID.
    Use this when the user wants to delete or remove a task entirely
    (not just mark it done). This action cannot be undone.
    The task_id must be the integer ID shown in list_todos.
    """
    todos = _load_todos()
    original_count = len(todos)

    updated = [t for t in todos if t["id"] != task_id]

    if len(updated) == original_count:
        return f"Error: No task found with ID {task_id}. Use list_todos to see valid IDs."

    removed = next(t for t in todos if t["id"] == task_id)
    _save_todos(updated)

    return (
        f"🗑️  Task deleted.\n"
        f"   ID   : {removed['id']}\n"
        f"   Task : {removed['task']}"
    )


# ── Start the server ──────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")
