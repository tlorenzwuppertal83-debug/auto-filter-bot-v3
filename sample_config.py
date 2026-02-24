# Bot information
SESSION = 'telegram-search-bot'
USER_SESSION = 'user-session'
API_ID = 12345
API_HASH = 'your_api_hash_here'
BOT_TOKEN = 'your_bot_token_here'
USERBOT_STRING_SESSION = 'session_string'

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = False

# Admins, Channels & Users
ADMINS = [123456789]
CHANNELS = [-100123456789]
AUTH_USERS = []
AUTH_CHANNEL = None

# MongoDB information
DATABASE_URI = "mongodb://localhost:27017"
DATABASE_NAME = 'telegram_database'
COLLECTION_NAME = 'telegram_files'

# Messages
START_MSG = """
Hi! I am a Telegram Media Search Bot.
Send me a file name to search.
"""

SHARE_BUTTON_TEXT = 'Share this bot'
INVITE_MSG = 'Please join the group to use this bot'