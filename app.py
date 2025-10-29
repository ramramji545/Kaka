import os
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from config import BOT_TOKEN, CHANNEL_ID, WEBHOOK_URL, PORT
from utils.telegram_utils import forward_to_channel

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global application instance
application = None

def create_application():
    """Create and configure the Telegram application."""
    global application
    if application is None:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        
        # Handle all media types
        application.add_handler(MessageHandler(
            filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE,
            handle_media
        ))
        
        # Handle text messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logger.info("✅ Telegram application created successfully")
    
    return application

async def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_text = (
        f"👋 Hello {user.first_name}!\n\n"
        "🤖 I'm a file forwarding bot.\n"
        "📁 Send me any file (document, photo, video, audio, etc.) and I'll automatically forward it to the channel.\n\n"
        "✅ Supported files:\n"
        "• Documents (PDF, TXT, ZIP, etc.)\n"
        "• Photos (JPG, PNG, etc.)\n"
        "• Videos (MP4, AVI, etc.)\n"
        "• Audio files (MP3, etc.)\n"
        "• And more!\n\n"
        "📤 Just send any file to get started!"
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📖 **How to use this bot:**\n\n"
        "1. Send any file (document, photo, video, audio)\n"
        "2. I'll automatically forward it to the channel\n"
        "3. You'll get a confirmation message\n\n"
        "📁 **Supported file types:**\n"
        "• All types of documents\n"
        "• Images and photos\n"
        "• Videos\n"
        "• Audio files\n"
        "• And more!\n\n"
        "❓ **Need help?** Contact the administrator."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle text messages."""
    text = (
        "📤 Please send me a file to forward to the channel.\n\n"
        "Supported files:\n"
        "• Documents (PDF, TXT, ZIP, etc.)\n"
        "• Photos\n"
        "• Videos\n"
        "• Audio files\n\n"
        "Use /help for more information."
    )
    await update.message.reply_text(text)

async def handle_media(update: Update, context: CallbackContext) -> None:
    """Handle all types of media files and forward to channel."""
    try:
        message = update.message
        chat_id = message.chat_id
        
        # Forward the message to channel
        success = await forward_to_channel(update, context)
        
        if success:
            await message.reply_text("✅ File successfully forwarded to channel!")
        else:
            await message.reply_text("❌ Failed to forward file to channel. Please try again.")
            
    except Exception as e:
        logger.error(f"Error handling media: {e}")
        await update.message.reply_text("❌ An error occurred while processing your file.")

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "Telegram File to Channel Bot",
        "version": "1.0"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram."""
    try:
        # Create application if not exists
        app = create_application()
        
        # Process update
        update = Update.de_json(request.get_json(), app.bot)
        app.update_queue.put(update)
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set webhook URL manually."""
    try:
        if not WEBHOOK_URL:
            return jsonify({"error": "WEBHOOK_URL not configured"}), 400
            
        app = create_application()
        
        # Set webhook
        success = app.bot.set_webhook(WEBHOOK_URL)
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Webhook set to {WEBHOOK_URL}",
                "webhook_info": app.bot.get_webhook_info().to_dict()
            })
        else:
            return jsonify({"error": "Failed to set webhook"}), 500
            
    except Exception as e:
        logger.error(f"Set webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render."""
    return jsonify({"status": "healthy", "service": "telegram-bot"})

def main():
    """Start the application."""
    try:
        # Create application
        app_creator = create_application()
        
        # Set webhook if URL is provided
        if WEBHOOK_URL:
            app_creator.bot.set_webhook(WEBHOOK_URL)
            logger.info(f"✅ Webhook set to: {WEBHOOK_URL}")
            print(f"✅ Webhook set to: {WEBHOOK_URL}")
        else:
            logger.warning("⚠️ WEBHOOK_URL not set, using polling mode")
            print("⚠️ WEBHOOK_URL not set")
        
        # For Render, we don't run polling, Flask app handles webhooks
        print("✅ Bot started successfully in webhook mode")
        print(f"📍 Server running on port {PORT}")
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
    # Note: We don't run Flask directly in production
    # Render will use gunicorn to run the app