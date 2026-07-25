A very simple architecture looks like this:

```text
Python App  --->  Ollama API  --->  Local AI Model
```

For example:

- Python app → user interface / logic
- Ollama → runs the model locally
- Model → Llama 3, Mistral, DeepSeek, Gemma, etc.

### Step 1 — Install Ollama

Download and install:

Ollama Official Website

After installing, verify:

```bash
ollama --version
```

### Step 2 — Pull a Model

Example using Llama 3:

```bash
ollama pull llama3
```

Run the model:

```bash
ollama run llama3
```

Now the AI model is running locally.

### Step 3 — Install Python Library

Create a project folder:

```bash
mkdir ollama-python-app
cd ollama-python-app
```

Install dependencies:

```bash
pip install ollama
```

### Step 4 — Write Your First Python AI App

Create:

`app.py`

Code:

```python
import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {
            'role': 'user',
            'content': 'Explain Python in simple words'
        }
    ]
)

print(response['message']['content'])
```

Run:

```bash
python app.py
```

**Output Example**
```text
Python is a programming language used to build websites,
AI systems, automation scripts, games, and more.
It is beginner friendly and easy to read.
```

### Step 5 — Build a Basic AI Chat Application

Now let’s create a small chatbot.

```python
import ollama

print("AI Chatbot Started")
print("Type 'exit' to stop")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': user_input
            }
        ]
    )

    print("\nAI:", response['message']['content'])
```

Run:

```bash
python app.py
```

**Example Conversation**
```text
You: What is machine learning?

AI: Machine learning is a method where computers learn
patterns from data without being explicitly programmed.
```

### Step 6 — Build a Simple Web Application

Install Flask:

```bash
pip install flask ollama
```

Create:

`webapp.py`

Code:

```python
from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.json['message']

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': user_message
            }
        ]
    )

    return jsonify({
        'response': response['message']['content']
    })

if __name__ == '__main__':
    app.run(debug=True)
```

Run:

```bash
python webapp.py
```

Server starts at:

`http://127.0.0.1:5000`

**Test Using Curl**
```bash
curl -X POST http://127.0.0.1:5000/chat \
-H "Content-Type: application/json" \
-d '{"message":"Tell me a joke"}'
```

### Step 7 — Real Projects You Can Build

Using Ollama + Python:

| Project | Description |
|---|---|
| AI Chatbot | Local ChatGPT |
| Resume Analyzer | Analyze resumes |
| AI Coding Assistant | Code generation |
| PDF Question Answering | Chat with documents |
| Voice Assistant | Speech + AI |
| AI Teacher | Explain concepts |
| AI Notes Generator | Convert lectures to notes |
| AI Trading Assistant | Market analysis |
| AI Fitness Coach | Workout recommendations |
| AI LMS Assistant | Learning companion |

Example:

```bash
ollama pull deepseek-coder
```

### Google Colab reference
https://colab.research.google.com/drive/1ukIAk_ytgqtrYqaxncrNnNmFUl3xeWbi?usp=sharing
