import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get token
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set!")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! 👋\n\n"
        f"I'm your notification bot. I can send you alerts!\n\n"
        f"Commands:\n"
        f"/start - Show this message\n"
        f"/help - Show help\n"
        f"/ping - Check if I'm alive\n"
        f"/echo <message> - Echo your message"
    )
    logger.info(f"User {user.first_name} started the bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /help is issued."""
    await update.message.reply_text(
        "🤖 Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/ping - Check if bot is alive\n"
        "/echo <message> - Echo your message\n\n"
        "Just send me any message and I'll reply!"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to /ping command."""
    await update.message.reply_text("🏓 Pong! I'm alive and working!")
    logger.info("Ping command received")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user's message."""
    if context.args:
        message = ' '.join(context.args)
        await update.message.reply_text(f"🔊 You said: {message}")
    else:
        await update.message.reply_text("Please provide a message: /echo <message>")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages."""
    message_text = update.message.text
    user = update.effective_user
    
    logger.info(f"Received message from {user.first_name}: {message_text}")
    
    # Send a response
    await update.message.reply_text(
        f"📨 I received your message!\n\n"
        f"Your message: {message_text}\n\n"
        f"Use /help to see available commands."
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    logger.info("Starting Telegram Bot...")
    logger.info(f"Using token: {TOKEN[:10]}...")  # Log first 10 chars for debugging
    
    try:
        # Create the Application
        application = Application.builder().token(TOKEN).build()
        
        # Register command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("ping", ping))
        application.add_handler(CommandHandler("echo", echo))
        
        # Register message handler for all text messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Register error handler
        application.add_error_handler(error_handler)
        
        # Start the bot
        logger.info("Bot is starting to poll for updates...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    main()
