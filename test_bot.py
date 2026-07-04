import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')
        reply = f"You said: {text}"
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={'chat_id': chat_id, 'text': reply}
        )
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
