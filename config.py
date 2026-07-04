import os

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ ERROR: BOT_TOKEN environment variable not set!")
    print("❌ Please add BOT_TOKEN to Railway Variables")
    # Don't exit - let the bot try to start anyway
    # The bot will fail gracefully
else:
    print("✅ BOT_TOKEN loaded successfully!")
