
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat/send', methods=['POST'])
def chat_send():
    data = request.get_json()
    user_message = data.get('message')
    
    # Here you can integrate with your AI model/API
    # For now, let's send a simple response
    response = f"You said: {user_message}"
    
    return jsonify({'response': response})
