import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("")
API_ID = os.getenv("26331872")
API_HASH = os.getenv("c93589620441707c37c5683a02eea54e")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1003161993313")

# Validate required environment variables
required_vars = ["BOT_TOKEN", "API_ID", "API_HASH"]
for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Missing required environment variable: {var}")

# Webhook Configuration for Render
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/webhook" if RENDER_EXTERNAL_URL else None
PORT = int(os.getenv("PORT", 10000))

# Bot settings
ADMIN_IDS = []  # Add admin user IDs if needed
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

print("✅ Configuration loaded successfully")
print(f"🤖 Bot Token: {BOT_TOKEN[:10]}...")
print(f"🔗 Channel ID: {CHANNEL_ID}")
print(f"🌐 Webhook URL: {WEBHOOK_URL}")
