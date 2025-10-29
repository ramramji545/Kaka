import logging
from telegram import Update
from telegram.ext import CallbackContext
from config import CHANNEL_ID

logger = logging.getLogger(__name__)

async def forward_to_channel(update: Update, context: CallbackContext) -> bool:
    """Forward any media message to the channel."""
    try:
        message = update.message
        
        if not message:
            return False
        
        # Forward the message to channel
        forwarded_message = await message.forward(chat_id=CHANNEL_ID)
        
        if forwarded_message:
            logger.info(f"✅ File forwarded to channel {CHANNEL_ID}")
            return True
        else:
            logger.error("❌ Failed to forward message to channel")
            return False
            
    except Exception as e:
        logger.error(f"Error forwarding to channel: {e}")
        return False
