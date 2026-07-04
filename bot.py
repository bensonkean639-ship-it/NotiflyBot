import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN not set!")

# Store the bot's webhook URL
WEBHOOK_URL = None

@app.route('/', methods=['GET'])
def index():
    """Home page."""
    return jsonify({
        'status': 'ok',
        'message': 'Telegram Bot is running',
        'token_configured': bool(TOKEN),
        'webhook_configured': bool(WEBHOOK_URL)
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages from Telegram."""
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
            text = message.get('text', '').lower()
            
            # Handle commands
            if text == '/start':
                reply = "👋 Hello! I'm your notification bot!\n\nCommands:\n/ping - Check if I'm alive\n/help - Show this message"
            elif text == '/ping':
                reply = "🏓 Pong! I'm alive and working!"
            elif text == '/help':
                reply = "🤖 Available commands:\n/start - Start the bot\n/ping - Check if I'm alive\n/help - Show this help"
            else:
                reply = f"📨 I received: {text}\n\nSend /ping to check if I'm alive."
            
            # Send response
            send_telegram_message(chat_id, reply)
        
        return jsonify({'status': 'ok'}), 200
        
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def send_telegram_message(chat_id, text):
    """Send a message to Telegram."""
    if not TOKEN:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        logging.info(f"Message sent: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return False

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set the webhook URL."""
    global WEBHOOK_URL
    
    if not TOKEN:
        return jsonify({'error': 'Token not configured'}), 500
    
    try:
        # Get the public URL
        # Railway provides RAILWAY_STATIC_URL
        public_url = os.getenv('RAILWAY_STATIC_URL')
        
        # If not set, use the host from the request
        if not public_url:
            public_url = request.host_url
        
        # Remove trailing slash if present
        if public_url.endswith('/'):
            public_url = public_url[:-1]
        
        # Build the webhook URL
        webhook_url = f"{public_url}/webhook"
        WEBHOOK_URL = webhook_url
        
        # Set the webhook
        url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
        payload = {'url': webhook_url}
        response = requests.post(url, json=payload, timeout=10)
        
        logging.info(f"Webhook set to: {webhook_url}")
        
        return jsonify({
            'status': 'success',
            'webhook_url': webhook_url,
            'response': response.json()
        })
        
    except Exception as e:
        logging.error(f"Error setting webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Delete the webhook."""
    if not TOKEN:
        return jsonify({'error': 'Token not configured'}), 500
    
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
        response = requests.post(url, timeout=10)
        
        return jsonify({
            'status': 'success',
            'response': response.json()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send_test', methods=['GET'])
def send_test():
    """Send a test message."""
    if not TOKEN:
        return jsonify({'error': 'Token not configured'}), 500
    
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not chat_id:
        return jsonify({'error': 'TELEGRAM_CHAT_ID not set'}), 500
    
    try:
        success = send_telegram_message(chat_id, "✅ Test message from Railway!")
        
        if success:
            return jsonify({'status': 'success', 'message': 'Test message sent'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
