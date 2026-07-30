# pyrefly: ignore [missing-import]
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