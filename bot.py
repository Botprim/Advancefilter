import sys
import glob
import importlib
import logging
import asyncio
from pathlib import Path
from pyrogram import Client, idle, __version__
from pyrogram.raw.all import layer
from aiohttp import web
import pytz
from datetime import datetime, date

# Importing required modules
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import *
from utils import temp
from plugins import web_server
from lazybot import LazyPrincessBot
from util.keepalive import ping_server
from lazybot.clients import initialize_clients

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

# Load Plugins
ppath = "plugins/*.py"
files = glob.glob(ppath)

async def Lazy_start():
    print("\n✅ Initializing Lazy Bot...")

    # Start Bot
    await LazyPrincessBot.start()
    
    # Get Bot Info
    bot_info = await LazyPrincessBot.get_me()
    LazyPrincessBot.username = bot_info.username

    # Initialize Clients
    await initialize_clients()

    # Load Plugins
    for name in files:
        with open(name) as f:
            plugin_name = Path(f.name).stem
            spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}", f"plugins/{plugin_name}.py")
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)
            sys.modules[f"plugins.{plugin_name}"] = plugin_module
            print(f"✅ Loaded Plugin => {plugin_name}")

    # Keep-Alive Task for Koyeb/Heroku
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # Fetch Banned Users & Chats
    temp.BANNED_USERS, temp.BANNED_CHATS = await db.get_banned()
    
    # Ensure Indexes
    await Media.ensure_indexes()

    # Store Bot Info
    temp.ME = bot_info.id
    temp.U_NAME = bot_info.username
    temp.B_NAME = bot_info.first_name

    logging.info(f"🤖 {bot_info.first_name} | Pyrogram v{__version__} | Layer {layer} | Started as {bot_info.username}")

    # Send Restart Message (Handle LOG_CHANNEL Error)
    if LOG_CHANNEL:
        try:
            tz = pytz.timezone("Asia/Kolkata")
            now = datetime.now(tz).strftime("%H:%M:%S %p")
            today = date.today()
            await LazyPrincessBot.send_message(
                chat_id=int(LOG_CHANNEL),
                text=f"✅ Bot Restarted on {today} at {now} (IST)"
            )
        except Exception as e:
            logging.warning(f"⚠️ LOG_CHANNEL Error: {e}")

    # Start Web Server (for Koyeb)
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", PORT).start()

    await idle()
    await LazyPrincessBot.stop()
    print("Bot Stopped.")

if __name__ == "__main__":
    asyncio.run(Lazy_start())  # ✅ Correct Event Loop Handling
