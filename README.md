# Telegram Notification Bot

A simple, lightweight Telegram bot for sending notifications.

## Features
- Send notifications to your Telegram chat
- Support for HTML formatting (bold, italic, etc.)
- Environment variables for secure token management
- Production-ready for Railway deployment

## Setup

### 1. Get Your Credentials
1. Create a bot with [@BotFather](https://t.me/botfather) on Telegram
2. Copy your bot token
3. Start a chat with your bot and send a message
4. Visit: `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
5. Copy your `chat_id` from the response

### 2. Deploy on Railway
1. Push this code to GitHub
2. Connect your repository to Railway
3. Add environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat ID

### 3. Usage
```python
from bot import send_notification

send_notification("Your notification message here")
