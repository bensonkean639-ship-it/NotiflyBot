import os
import logging
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Get environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    """Send message to Telegram."""
    if not TOKEN or not CHAT_ID:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return False

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'Telegram Notification Bot is running',
        'token_configured': bool(TOKEN),
        'chat_id_configured': bool(CHAT_ID)
    })

@app.route('/send', methods=['POST'])
def send_message():
    """API endpoint to send a notification."""
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Missing message parameter'}), 400
        
        success = send_telegram_message(message)
        
        if success:
            return jsonify({'status': 'success', 'message': 'Notification sent'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to send'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Detailed health check."""
    return jsonify({
        'status': 'healthy',
        'telegram_token': 'configured' if TOKEN else 'missing',
        'chat_id': 'configured' if CHAT_ID else 'missing'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
