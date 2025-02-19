import re
from os import environ, getenv
from Script import script  

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default=False):
    return value.lower() in ["true", "yes", "1", "enable", "y"] if isinstance(value, str) else default

# ✅ Bot Information
SESSION = "Media_search"
API_ID = 22724700
API_HASH = "9acec40ee27d6b12a52b5e97c2402678"
BOT_TOKEN = "6659315454:AAELhaRCB5yoHkQ9HJZwzW5YCIot4gM3j8g"

# ✅ Bot Settings
CACHE_TIME = 300
USE_CAPTION_FILTER = True

PICS = [
    "https://graph.org/file/0c9c9bd9b7d7530e405bf.jpg",
    "https://graph.org/file/81d02ba222450df17a4dd.jpg",
    "https://graph.org/file/e02c47f6f3dbdc41cdcf0.jpg",
]
NOR_IMG = "https://te.legra.ph/file/a27dc8fe434e6b846b0f8.jpg"

# ✅ Admins, Channels & Users
ADMINS = [5002159457]
CHANNELS = [-1001545302652, -1001912376797, -1001831546731]
AUTH_USERS = ADMINS
PREMIUM_USER = []
AUTH_CHANNEL = -1002428743245
AUTH_GROUPS = None

# ✅ MongoDB Information
DATABASE_URI = "mongodb+srv://Kismisbotz:Kismisbotz@cluster0.a5veje6.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "RIONETWORKS"
COLLECTION_NAME = "Telegram_files"

# ✅ Other Settings
LOG_CHANNEL = -1002323650440
SHORTLINK_URL = "modijiurl.com"
SHORTLINK_API = "37f43b8742b61d26dc44f930e1b25c9c9f314779"
IS_SHORTLINK = True
MAX_B_TN = 5
PORT = 8080

# ✅ Online Stream and Download
ON_HEROKU = False
APP_NAME = None
FQDN = "cooing-amalia-friendship-60627208.koyeb.app"
URL = f"https://{FQDN}/"

# ✅ Feature Flags
IMDB = True
AUTO_FFILTER = True
AUTO_DELETE = True
SINGLE_BUTTON = True

# ✅ Other Constants
LANGUAGES = ["malayalam", "mal", "tamil", "tam", "english", "eng", "hindi", "hin", "telugu", "tel", "kannada", "kan"]
SEASONS = ["season 1", "season 2", "season 3", "season 4", "season 5"]

# ✅ Log Configurations
LOG_STR = "Current Configurations are:-\n"
LOG_STR += "✅ IMDB Results are enabled.\n"
LOG_STR += "✅ Auto Filter is enabled.\n"
LOG_STR += "✅ Auto Delete is enabled.\n"
LOG_STR += f"✅ Bot URL: {URL}\n"
