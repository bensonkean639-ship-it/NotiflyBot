import os
import requests
import logging
import time
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

# Debug: Check if variables exist
logger.info(f"TOKEN exists: {bool(TOKEN)}")
logger.info(f"CHAT_ID exists: {bool(CHAT_ID)}")

if not TOKEN or not CHAT_ID:
    logger.error("Missing required environment variables!")
    logger.error("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID")
    # Don't exit, let it try to run anyway for debugging
else:
    logger.info("Environment variables loaded successfully")

URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage" if TOKEN else None

def send_notification(message, parse_mode='HTML'):
    """
    Send a notification message to the configured Telegram chat.
    """
    if not TOKEN or not CHAT_ID:
        logger.error("Cannot send: Missing token or chat ID")
        return False
    
    try:
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': True
        }
        
        response = requests.post(URL, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Notification sent successfully")
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

if __name__ == "__main__":
    logger.info("Starting Telegram Notification Bot...")
    
    # Send a test notification on startup
    if TOKEN and CHAT_ID:
        if test_bot():
            logger.info("✅ Bot started successfully!")
        else:
            logger.warning("⚠️ Bot started but failed to send test notification")
    else:
        logger.warning("⚠️ Bot started but missing credentials")
    
    # Keep the bot running
    try:
        while True:
            # Keep the bot alive
            # You can add your custom notification logic here
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
