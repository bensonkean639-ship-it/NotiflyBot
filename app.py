import os
import logging
from flask import Flask, request, jsonify
import requests
import subprocess
import sys
import threading
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'Telegram Bot is running',
        'token_configured': bool(TOKEN)
    })

@app.route('/health', methods=['GET'])
def health():
    """Detailed health check."""
    return jsonify({
        'status': 'healthy',
        'telegram_token': 'configured' if TOKEN else 'missing',
        'bot_online': True
    })

@app.route('/send', methods=['GET', 'POST'])
def send_message():
    """Send a notification message."""
    if not TOKEN or not CHAT_ID:
        return jsonify({'error': 'Missing credentials'}), 500
    
    try:
        if request.method == 'GET':
            message = request.args.get('message', 'Test notification!')
        else:
            data = request.get_json()
            message = data.get('message', 'Test notification!')
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'Notification sent'}), 200
        else:
            return jsonify({'status': 'error', 'message': response.text}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_bot():
    """Run the bot in a separate thread."""
    from bot import main
    main()

if __name__ == '__main__':
    # Start the bot in a background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Run the web server
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
