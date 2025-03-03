import sys
import glob
import importlib
from pathlib import Path
import logging
import asyncio
from pyrogram import Client, idle, __version__
from pyrogram.raw.all import layer
from aiohttp import web
import pytz
from datetime import date, datetime

# Import Local Modules
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

# Plugin Loader
ppath = "plugins/*.py"
files = glob.glob(ppath)

# Start Bot
LazyPrincessBot.start()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def Lazy_start():
    print("\n✅ Initializing Lazy Bot...")
    
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

    # Keep-Alive Task for Heroku/Koyeb
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # Fetch Banned Users & Chats
    temp.BANNED_USERS, temp.BANNED_CHATS = await db.get_banned()
    
    # Ensure Indexes
    await Media.ensure_indexes()

    # Store Bot Info
    me = await LazyPrincessBot.get_me()
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    LazyPrincessBot.username = f'@{me.username}'

    logging.info(f"🤖 {me.first_name} | Pyrogram v{__version__} | Layer {layer} | Started as {me.username}")

    # LOG_CHANNEL Fix (Optional)
    if LOG_CHANNEL:
        try:
            tz = pytz.timezone("Asia/Kolkata")
            now = datetime.now(tz).strftime("%H:%M:%S %p")
            today = date.today()
            await LazyPrincessBot.send_message(
                chat_id=LOG_CHANNEL,
                text=f"✅ Bot Restarted on {today} at {now} (IST)"
            )
        except Exception as e:
            logging.warning(f"⚠️ LOG_CHANNEL Error: {e}")

    # Start Web Server (for Koyeb)
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", PORT).start()

    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(Lazy_start())
    except KeyboardInterrupt:
        logging.info("🛑 Bot Stopped. Goodbye! 👋")
