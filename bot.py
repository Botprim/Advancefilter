import sys
import glob
import importlib
from pathlib import Path
import logging
import logging.config
import asyncio
from pyrogram import Client, __version__, idle
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db  # ✅ अब पूरा Database Object Import कर रहे हैं
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script
from datetime import date, datetime
import pytz
from aiohttp import web
from plugins import web_server
from lazybot import LazyPrincessBot
from util.keepalive import ping_server
from lazybot.clients import initialize_clients

# ✅ Users और Groups Collection को Access करें
users_collection = db.col  # Users Collection
chats_collection = db.grp  # Groups Collection

# ✅ Logging Setup
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

# ✅ Plugins Path
ppath = "plugins/*.py"
files = glob.glob(ppath)

# ✅ Fix: Correct Asyncio Event Loop Setup
async def Lazy_start():
    print('\nInitializing Lazy Bot')

    bot_info = await LazyPrincessBot.get_me()
    LazyPrincessBot.username = bot_info.username

    await initialize_clients()

    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"plugins/{plugin_name}.py")
            import_path = "plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["plugins." + plugin_name] = load
            print("Lazy Imported => " + plugin_name)

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # ✅ Fix: Ensure MongoDB Uses the Correct Event Loop
    loop = asyncio.get_running_loop()
    db.get_io_loop = loop  

    b_users, b_chats = [], []
    async for user in users_collection.find({"banned": True}):
        b_users.append(user["id"])
    async for chat in chats_collection.find({"banned": True}):
        b_chats.append(chat["id"])

    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats
    await Media.ensure_indexes()

    me = await LazyPrincessBot.get_me()
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    LazyPrincessBot.username = '@' + me.username

    logging.info(f"{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
    logging.info(LOG_STR)
    logging.info(script.LOGO)

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")

    # ✅ Fix: LOG_CHANNEL Issue
    try:
        if LOG_CHANNEL:
            await LazyPrincessBot.send_message(chat_id=int(LOG_CHANNEL), text="Bot restarted successfully!")
    except Exception as e:
        print(f"LOG_CHANNEL Error: {e} - Check if the ID is correct and bot is admin.")

    # ✅ Fix: Web Server Startup Optimization
    try:
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        print("Web server started successfully!")
    except Exception as e:
        print(f"Error in starting web server: {e}")

    await idle()

# ✅ Fix: Correctly Start the Bot Without Event Loop Conflict
async def main():
    await LazyPrincessBot.start()  # ✅ Ensure bot starts inside the correct loop
    await Lazy_start()

if __name__ == "__main__":
    asyncio.run(main())  # ✅ Now the bot and async functions share the same event loop
