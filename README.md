# 🤖 3-Day GenAI Workshop — EEE 
 
A beginner-friendly, hands-on Generative AI workshop designed for **III Year B.E. EEE** students — no prior coding or AI background required. Over 3 days, you'll go from Python basics to building your own local RAG + Agent-based AI assistant.
 
> 💡 Every session includes a plain-language explanation, a hands-on task with a complete working solution, and assignments to practice on your own — including a few just-for-fun, non-engineering ones.
 
---
 
## 📅 Table of Contents
 
| Day | Forenoon | Afternoon |
|---|---|---|
| [**Day 1**](#day-1--getting-started-with-ai--python) | Python Basics · Prompt Engineering | AI Tokenizer & Transformer |
| [**Day 2**](#day-2--running-ai-models-locally--basic-machine-learning) | Local LLM Architecture · Pulling & Running Models (Ollama – Gemma) | Machine Learning Basics — Supervised Learning (Matplotlib & Scikit-learn) |
| [**Day 3**](#day-3--advanced-ai-rag--agentic-ai) | Retrieval-Augmented Generation (RAG) Pipeline | Agentic AI & MCP + 🎓 **Final Project** |
 
---
 
## Day 1 — Getting Started with AI & Python
 
### Forenoon
| Topic | What it means (in simple terms) |
|---|---|
| **Python Basics** | A simple, English-like programming language — write step-by-step instructions for the computer, like a recipe. |
| **Prompt Engineering** | Learning how to ask an AI clearly so you get better, more accurate answers. |
 
### Afternoon
| Topic | What it means (in simple terms) |
|---|---|
| **AI Tokenizer** | Breaks a sentence into small pieces ("tokens") before the AI can process it — like sampling a signal into discrete values. |
| **Transformer** | The core AI "engine" design that looks at all tokens together to understand relationships between words. |
 
### 🔧 Hands-on
- [ ] Ohm's Law calculator (Python basics)
- [ ] Voltage-drop loop across 5 series resistors
- [ ] Prompt Engineering: same question, 3 prompt styles — compare results
- [ ] Tokenizer playground — tokenize an EEE sentence & compare token counts
### 📝 Assignments
1. Ohm's Law for 3 circuits (loop-based)
2. AC RMS → Peak voltage converter
3. Prompt Engineering practice (vague vs detailed vs role-based prompt)
4. Tokenizer comparison table (word count vs token count)
5. Draw & label the AI pipeline (Input → Tokenizer → Transformer → Output)
### 🎉 Bonus (General Interest, Non-EEE)
- **Hands-on:** Number Guessing Game · AI Persona Play (pirate / 5-year-old / professor prompts)
- **Assignments:** FizzBuzz Challenge · Rock-Paper-Scissors Game · Poem in 3 Styles
---
 
## Day 2 — Running AI Models Locally & Basic Machine Learning
 
### Forenoon
| Topic | What it means (in simple terms) |
|---|---|
| **Local LLM Architecture** | Running an AI language model on your own machine instead of over the internet. |
| **Pulling Models (Ollama, Gemma)** | Ollama lets you download and run free AI models locally, offline. |
 
### Afternoon
| Topic | What it means (in simple terms) |
|---|---|
| **Machine Learning — Supervised Learning** | Teaching a computer to find patterns from example input–output pairs. |
| **Matplotlib & Scikit-learn (Google Colab)** | Tools to plot graphs and train ready-made ML models, run for free in the browser. |
 
### 🔧 Hands-on
- [ ] Install Ollama, pull & run the `gemma:2b` model
- [ ] Call the local model from Python (`requests` → `localhost:11434`)
- [ ] Predict electricity load from temperature using Linear Regression
- [ ] Plot actual vs predicted values + evaluate error (MAE)
### 📝 Assignments
1. Ask the local model 3 subject-related questions & record response time
2. Plot diode V-I characteristics using matplotlib
3. Extend to Multiple Linear Regression (Temperature + Humidity → Load)
4. Error analysis — plot (Actual − Predicted) as a bar chart
5. Short note: one real use of ML in electrical/power engineering
### 🎉 Bonus (General Interest, Non-EEE)
- **Hands-on:** Classify Iris flowers with KNN (the "Hello World" of ML) · Give your local AI a fun personality
- **Assignments:** Exam Score Predictor · Flower Classifier tuning (try k = 1, 5, 9) · Design your own chatbot persona
---
 
## Day 3 — Advanced AI: RAG & Agentic AI
 
### Forenoon
| Topic | What it means (in simple terms) |
|---|---|
| **Retrieval-Augmented Generation (RAG)** | The AI first retrieves relevant info from your own documents, then answers based on that — like an open-book exam. |
 
### Afternoon
| Topic | What it means (in simple terms) |
|---|---|
| **Agentic AI** | An AI that can take multi-step actions to complete a task, not just answer a question. |
| **MCP (Model Context Protocol)** | A standard way to connect an AI model to outside tools, files, and databases. |
 
### 🔧 Hands-on
- [ ] Build a mini RAG pipeline (TF-IDF retrieval + local-model generation) on your own notes
- [ ] Build a simple agent that queries a maintenance-log dataset and answers status questions
### 🎉 Bonus (General Interest, Non-EEE)
- **Hands-on:** Movie Recommender Agent (same RAG + Agent pattern, applied to a movie dataset)
### 🎓 Final Project (in place of assignments)
Build **"AI-Powered Smart Assistant"** — a Colab notebook combining a RAG component (answers from a document) and an Agent/tool component (answers from a dataset) into one assistant.
 
- **Team size:** 3–4 students
- **Default theme:** Electrical Lab / Department Assistant
- **Optional alternative themes:** Campus FAQ Assistant · Movie/Book Recommendation Assistant · Personal Study Assistant
- **Deliverables:** working notebook · document chunks + dataset used · 5+ test Q&A · 1-page report with pipeline diagram · 5-min live demo
- **Evaluation:** RAG component (20) · Agent/tool component (20) · Combined logic (20) · Code clarity (15) · Report (10) · Demo (15) · Bonus +5 for a third tool
---
 
## 🛠️ Prerequisites & Setup
 
| Tool | Purpose | Link |
|---|---|---|
| Google Colab | Run all Python code, no install needed | https://colab.research.google.com |
| Ollama | Run AI models locally (Day 2 onward) | https://ollama.com |
| Python 3.x | Local scripting (optional, Colab covers most needs) | https://python.org |
 
```bash
# One-time setup for local model (Day 2)
ollama pull gemma:2b
ollama run gemma:2b
```
 
---
 
## 📁 Suggested Repository Structure
 
```
genai-workshop-eee/
├── README.md
├── day1-python-prompting/
│   ├── ohms_law_calculator.ipynb
│   ├── voltage_drop_loop.ipynb
│   └── prompt_engineering_notes.md
├── day2-local-llm-ml/
│   ├── ollama_setup.md
│   ├── load_prediction_regression.ipynb
│   └── iris_classification_bonus.ipynb
├── day3-rag-agents/
│   ├── mini_rag_pipeline.ipynb
│   ├── maintenance_agent.ipynb
│   └── movie_recommender_bonus.ipynb
└── final-project/
    └── README.md   # project brief, rubric, and submission template
```
 
---
 
## 📜 License
 
Add your preferred license here (e.g., MIT) — see [choosealicense.com](https://choosealicense.com/) if unsure.
