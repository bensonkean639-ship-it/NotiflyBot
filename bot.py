import os
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TOKEN or not CHAT_ID:
    logger.error("Missing required environment variables!")
    exit(1)

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_notification(message, parse_mode='HTML'):
    """
    Send a notification message to the configured Telegram chat.
    
    Args:
        message (str): The message to send
        parse_mode (str): 'HTML' or 'Markdown' for formatting
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': True
        }
        
        response = requests.post(URL, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Notification sent successfully: {message[:50]}...")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send notification: {e}")
        return False

def test_bot():
    """Send a test message to verify the bot is working."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_message = f"""
<b>🚀 Bot is Live!</b>

<i>Your Telegram notification bot is up and running!</i>
📅 Time: {timestamp}
✅ Status: Active

<b>Ready to receive notifications.</b>
    """
    return send_notification(test_message)

def main():
    """Main entry point for the bot."""
    logger.info("Starting Telegram Notification Bot...")
    
    # Send a test notification on startup
    if test_bot():
        logger.info("Bot started successfully!")
    else:
        logger.error("Bot failed to send startup notification!")
    
    # Keep the bot running
    # You can add scheduled tasks or other logic here
    import time
    try:
        while True:
            # Add your custom notification logic here
            # For example, check for new data, send alerts, etc.
            # This is where you'd add your scheduled tasks
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

if __name__ == "__main__":
    main()
