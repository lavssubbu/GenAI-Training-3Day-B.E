# pyrefly: ignore [missing-import]
from flask import Flask, request, jsonify
# pyrefly: ignore [missing-import]
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