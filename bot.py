import sys
import glob
import importlib
import logging
import asyncio
from pathlib import Path
from pyrogram import Client, idle, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import *
from utils import temp
from datetime import date, datetime
import pytz
from aiohttp import web
from plugins import web_server
from lazybot import LazyPrincessBot
from util.keepalive import ping_server
from lazybot.clients import initialize_clients

# Logging Configurations
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)

ppath = "plugins/*.py"
files = glob.glob(ppath)
LazyPrincessBot.start()

async def Lazy_start():
    print('\nInitializing Lazy Bot...')
    bot_info = await LazyPrincessBot.get_me()
    LazyPrincessBot.username = bot_info.username
    await initialize_clients()

    # Import Plugins
    for file in files:
        plugin_name = Path(file).stem
        import_path = f"plugins.{plugin_name}"
        try:
            importlib.import_module(import_path)
            print(f"Lazy Imported => {plugin_name}")
        except Exception as e:
            print(f"Failed to import {plugin_name}: {e}")

    # Ping Server if Hosted on Heroku
    if ON_HEROKU:
        asyncio.create_task(ping_server())

    # Load Banned Users & Chats
    b_users, b_chats = await db.get_banned()
    temp.BANNED_USERS = b_users
    temp.BANNED_CHATS = b_chats

    # Ensure Media Indexes
    await Media.ensure_indexes()

    # Set Bot Info
    me = await LazyPrincessBot.get_me()
    temp.ME = me.id
    temp.U_NAME = me.username
    temp.B_NAME = me.first_name
    LazyPrincessBot.username = '@' + me.username
    logging.info(f"{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
    
    # Send Startup Message
    try:
        if LOG_CHANNEL:
            tz = pytz.timezone('Asia/Kolkata')
            today = date.today()
            now = datetime.now(tz)
            time = now.strftime("%H:%M:%S %p")
            await LazyPrincessBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    except Exception as e:
        logging.error(f"Failed to send startup message to LOG_CHANNEL: {e}")

    # Start Web Server
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    
    # Keep Bot Running
    await idle()

if __name__ == '__main__':
    try:
        asyncio.run(Lazy_start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
