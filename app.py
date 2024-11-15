from flask import Flask, request, render_template, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Directly configure API key for Google Generative AI
api_key = "AIzaSyA1K66Ev9ruG8yj462G5xD6RSj34Q0QVNk"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

# Start chatbot session with detailed ZUT information in user history
chat_session = model.start_chat(
    history=[{
        "role": "user",
        "parts": [
            "You're a chatbot and you only answer about agriculture unless its a greeting, if someone asks something different just say i can only answer question about agriculture."
        ]
    }]
)

@app.route('/')
def home():
    return render_template('index.html')  # Home page for chatbot interface

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['message']
    response = chat_session.send_message(user_message)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
