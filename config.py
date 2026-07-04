import os

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    print("⚠️ WARNING: BOT_TOKEN not found in environment variables!")
    print("⚠️ Using placeholder token. The bot will not work!")
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
else:
    print("✅ BOT_TOKEN loaded successfully!")
