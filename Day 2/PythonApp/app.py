# pyrefly: ignore [missing-import]
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