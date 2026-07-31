# 1. What is Agentic AI?

### Traditional AI Chatbot

Normal chatbot:

```text
User → LLM → Response
```

**Example:**

You ask:
“Summarize this PDF”
LLM responds directly.

---

### Agentic AI

Agentic AI can:
*   think
*   plan
*   use tools
*   make decisions
*   execute tasks

**Example:**

User:
"Read all invoices from folder and calculate total"

Agent:
1. Finds files
2. Opens PDFs
3. Extracts text
4. Calculates totals
5. Generates report

This is an AI Agent.

---

# 2. Why Agentic AI is Needed

LLMs alone cannot:
*   access files
*   browse local folders
*   call APIs
*   use tools
*   remember workflows
*   automate tasks

Agentic AI solves this.

---

# 3. Real Industry Uses

| Industry | Agent Use |
| :--- | :--- |
| Banking | Document processing |
| HR | Resume screening |
| Healthcare | Medical summarization |
| IT Support | Automated troubleshooting |
| Education | AI teaching assistant |
| Manufacturing | Predictive maintenance workflows |

---

# 4. Architecture of Agentic AI

### Flow

```text
User Request
     ↓
  AI Agent
     ↓
Reasoning Engine
     ↓
Tool Selection
     ↓
 Execute Tool
     ↓
LLM Analyzes Result
     ↓
 Final Response
```

---

# 5. Local LLM with Ollama

## STEP 1 — Install Ollama

Download:
**[Ollama Official Website](https://ollama.com)**

Install model:
```bash
ollama pull llama3
```

Run model:
```bash
ollama run llama3
```

Test:
```text
Hello
```

## STEP 2 — Install Python Libraries

```bash
pip install langchain langchain-community ollama
```

Optional:
```bash
pip install pandas requests
```

---

# 5) How it works Code — BASIC AGENT WITH OLLAMA

Now we build a simple AI Agent.

**PROJECT:** AI Math Agent

### Capabilities:
*   Understand question
*   Decide tool
*   Use calculator
*   Return answer

### Folder Structure
```text
agentic_ai/
└── app.py
```

### CODE — app.py

```python
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.agents import AgentType
import math


# -----------------------------
# LOCAL LLM
# -----------------------------
llm = Ollama(model="llama3")


# -----------------------------
# TOOL 1 : Calculator
# -----------------------------
def calculator_tool(query):
    try:
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# TOOL 2 : Square Root
# -----------------------------
def sqrt_tool(query):
    try:
        number = float(query)
        return str(math.sqrt(number))
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# TOOLS LIST
# -----------------------------
tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for mathematical calculations"
    ),

    Tool(
        name="SquareRoot",
        func=sqrt_tool,
        description="Useful for square root calculations"
    )
]


# -----------------------------
# AGENT
# -----------------------------
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


# -----------------------------
# USER QUERY
# -----------------------------
query = input("Ask Something: ")

response = agent.run(query)

print("\nFINAL ANSWER:")
print(response)
```

---

# 6. How This Code Works (VERY IMPORTANT)

## PART 1 — Load Local LLM

```python
llm = Ollama(model="llama3")
```

This connects Python → Ollama → Local LLM.

### Meaning:
*   No cloud
*   No OpenAI
*   Fully local AI

## PART 2 — Tools

Agent becomes powerful using tools.

### Example:
```python
Tool(
    name="Calculator",
    func=calculator_tool,
    description="Useful for mathematical calculations"
)
```

The LLM reads the description and decides:
*   when to use it
*   how to use it

## PART 3 — Reasoning Agent

```python
agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
```

This enables:
*   reasoning
*   thinking
*   deciding tools

The agent follows:
*   Thought
*   Action
*   Observation
*   Final Answer

This is called: **ReAct Architecture**

## PART 4 — Agent Execution

**Input:**
```text
What is sqrt of 144?
```

Agent internally thinks:

> **Thought:**
> Need square root tool
>
> **Action:**
> SquareRoot
>
> **Observation:**
> 12
>
> **Final Answer:**
> 12

---

# 7. Run the Project

Run:
```bash
python app.py
```

**Example:**

Ask Something:
What is square root of 625?

Output:
```text
25
```

---

# 8. Upgrade the Agent (IMPORTANT)

Now let’s make it REAL AGENTIC AI.

### Add Internet Tool

```bash
pip install duckduckgo-search
```

**Tool:**
```python
from duckduckgo_search import DDGS

def search_web(query):
    results = DDGS().text(query, max_results=3)
    return str(results)
```

Now AI can:
*   search internet
*   reason
*   combine information

### Add File Reading Tool

```python
def read_file(filename):
    with open(filename, "r") as f:
        return f.read()
```

Now AI can:
*   read local files
*   summarize documents

### REAL AGENTIC SYSTEM

User:
"Read sales.txt and calculate total revenue"

Agent:
1. Opens file
2. Extracts values
3. Calculates total
4. Generates summary

THIS is production-style Agentic AI.

---

# 9. Agentic AI with GEMINI

Now same concept using Google Gemini.

## STEP 1 — Install

```bash
pip install google-generativeai
```

## STEP 2 — Get API Key

Get API key:
**[Google AI Studio](https://aistudio.google.com/)**

## STEP 3 — Gemini Agent Code

### app_gemini.py

```python
import google.generativeai as genai
import math


# --------------------------------
# CONFIGURE API
# --------------------------------
genai.configure(api_key="YOUR_API_KEY")


# --------------------------------
# LOAD MODEL
# --------------------------------
model = genai.GenerativeModel("gemini-1.5-flash")


# --------------------------------
# TOOLS
# --------------------------------
def calculator(query):
    try:
        return str(eval(query))
    except Exception as e:
        return str(e)


def square_root(query):
    try:
        return str(math.sqrt(float(query)))
    except Exception as e:
        return str(e)


# --------------------------------
# SIMPLE AGENT LOOP
# --------------------------------
while True:

    user = input("\nAsk: ")

    prompt = f"""
    You are an AI agent.

    Available tools:
    1. calculator
    2. square_root

    User query:
    {user}

    Decide:
    - Which tool to use
    - What input to pass
    """

    response = model.generate_content(prompt)

    answer = response.text

    print("\nAgent Thinking:")
    print(answer)
```

## Difference Between Ollama vs Gemini

| Feature | Ollama | Gemini |
| :--- | :--- | :--- |
| Runs Local | Yes | No |
| Internet Needed | No | Yes |
| Privacy | High | Medium |
| Speed | Depends on PC | Fast |
| Cost | Free | API based |
| Best For | Offline AI | Production AI |

---

# 10. Real Industry Agent Architecture

```text
Frontend
   ↓
FastAPI Backend
   ↓
Agent Framework
   ↓
LLM
   ↓
Tools
   ├── Database
   ├── APIs
   ├── Search
   ├── File System
   └── Vector DB
```

This connects directly with:
*   LangChain
*   RAG
*   AI Assistants
*   Autonomous Systems

Mentioned in your syllabus roadmap.

---

# 11. Mini Challenge

Build: **AI File Assistant**

### Capabilities:
*   Read txt files
*   Summarize files
*   Count words
*   Answer questions

---

# 12. Common Beginner Mistakes

| Mistake | Problem |
| :--- | :--- |
| Using huge models | System crashes |
| No tool descriptions | Agent confused |
| Very long prompts | Slow reasoning |
| No error handling | Agent fails |
| Blind eval() | Security issue |

---

# 13. Industry Best Practice

Instead of:
```python
eval(query)
```

Use:
*   SymPy
*   Restricted parser
*   Sandboxed execution

Because eval is dangerous in production.

---

# 14. Interview Questions

*   What is Agentic AI?
*   Difference between chatbot and AI agent?
*   What is ReAct architecture?
*   Why tools are important in agents?
*   Why local LLMs matter?
*   What is function calling?
*   Difference between RAG and Agents?

---

# 15. Homework

## Beginner Level

Build:
*   Calculator agent
*   Weather agent
*   File reader agent

## Intermediate Level

Build:
*   PDF chatbot
*   Multi-tool AI assistant
*   Research agent

## Advanced Level

Build:
*   Autonomous coding agent
*   AI workflow orchestrator
*   Multi-agent system
