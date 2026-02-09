import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
REQUIRED_CHANNEL = os.getenv("CHANNEL_ID")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/noventis_bots") 
