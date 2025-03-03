import sys
import glob
import importlib
import logging
import asyncio
from pathlib import Path
from pyrogram import Client, __version__, idle
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import *
from utils import temp
from plugins import web_server
from lazybot import LazyPrincessBot
from util.keepalive import ping_server
from lazybot.clients import initialize_clients
from datetime import date, datetime
import pytz
from aiohttp import web

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

# Initialize bot
LazyPrincessBot.start()
loop = asyncio.get_event_loop()

async def Lazy_start():
    print("\nInitializing Lazy Bot...")

    bot_info = await LazyPrincessBot.get_me()
    LazyPrincessBot.username = bot_info.username

    # Load Plugins
    plugin_path = "plugins/*.py"
    for file in glob.glob(plugin_path):
        module_name = Path(file).stem
        import_path = f"plugins.{module_name}"
        spec = importlib.util.spec_from_file_location(import_path, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[import_path] = module
        print(f"✅ Loaded Plugin => {module_name}")

    # Initialize Clients
    await initialize_clients()

    # Fetch banned users & chats
    temp.BANNED_USERS, temp.BANNED_CHATS = await db.get_banned()

    # Ensure Media indexes
    await Media.ensure_indexes()

    # Bot Details
    temp.ME = bot_info.id
    temp.U_NAME = bot_info.username
    temp.B_NAME = bot_info.first_name

    logging.info(f"🤖 {bot_info.first_name} | Pyrogram v{__version__} | Layer {layer} | Started as @{bot_info.username}")

    # Send bot startup message
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(tz).strftime("%H:%M:%S %p")
    await LazyPrincessBot.send_message(LOG_CHANNEL, f"✅ Bot Restarted at {now} (IST)")

    # Start Web Server
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", PORT).start()

    # Keep Bot Running
    await idle()

if __name__ == "__main__":
    try:
        loop.run_until_complete(Lazy_start())
    except KeyboardInterrupt:
        logging.info("❌ Service Stopped. Bye! 👋")
