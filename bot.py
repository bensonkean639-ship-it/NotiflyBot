import os
import logging
import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN not set!")
    # Don't exit, let it run for debugging

# Telegram API URLs
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else None

def send_telegram_message(chat_id, text):
    """Send a message to Telegram."""
    if not TELEGRAM_URL:
        return False
    
    try:
        url = f"{TELEGRAM_URL}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return False

@app.route('/', methods=['GET'])
def health():
    """Health check."""
    return jsonify({
        'status': 'ok',
        'message': 'Telegram Bot is running',
        'token_configured': bool(TOKEN),
        'webhook_ready': True
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram messages."""
    try:
        # Get the update from Telegram
        update = request.get_json()
        
        if not update:
            return jsonify({'status': 'error', 'message': 'No data'}), 400
        
        logging.info(f"Received update: {update}")
        
        # Check if it's a message
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '')
            
            # Handle commands
            if text == '/start':
                reply = "👋 Hello! I'm your notification bot!\n\nSend /ping to check if I'm alive."
            elif text == '/ping':
                reply = "🏓 Pong! I'm alive and working!"
            else:
                reply = f"📨 I received: {text}\n\nSend /ping to check if I'm alive."
            
            # Send response
            send_telegram_message(chat_id, reply)
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set the webhook URL."""
    if not TELEGRAM_URL:
        return jsonify({'error': 'Token not configured'}), 500
    
    try:
        # Get the public URL from Railway
        # Railway provides this via the RAILWAY_STATIC_URL or we can use the host
        public_url = os.getenv('RAILWAY_STATIC_URL')
        if not public_url:
            # Try to get it from the request
            public_url = request.host_url
            if public_url.startswith('http://'):
                public_url = public_url.replace('http://', 'https://')
        
        webhook_url = f"{public_url}webhook"
        
        # Set the webhook
        url = f"{TELEGRAM_URL}/setWebhook"
        payload = {'url': webhook_url}
        response = requests.post(url, json=payload, timeout=10)
        
        return jsonify({
            'status': 'success',
            'webhook_url': webhook_url,
            'response': response.json()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
