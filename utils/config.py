import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN in environment")

BINANCE_API_URL = os.getenv("BINANCE_API_URL", "https://api.binance.com/api/v3")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")