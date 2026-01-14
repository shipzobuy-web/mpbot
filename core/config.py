import os
from dotenv import load_dotenv

# Only needed for local testing
load_dotenv()

class Config:
    TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    PREFIX = os.getenv("BOT_PREFIX", "!")
    MONGO = os.getenv("MONGO_URI")
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    CREATOR = os.getenv("CREATOR_ID")
    SUPPORT_SERVER = os.getenv("SUPPORT_SERVER")
    VERSION = os.getenv("BOT_VERSION", "1.0")
