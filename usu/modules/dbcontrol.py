import asyncio

from pyrogram.enums import UserStatus
import random
from asyncio import sleep

import random
import re

from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import *
import os
import psutil
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from usu.config import OWNER_ID, DEVS

from usu import *

@ubot.on_message(filters.group & filters.user(DEVS) & filters.command("tes", ""))
async def _(client, message):
    emoji = ["🔥", "👻", "❤️‍🔥", "🗿", "😈", "🍓", "🙊", "🍌", "💩", "🎃", "🏆", "⚡"]
    random_emoji = random.choice(emoji)
    chat = message.chat.id
    id = message.id
    await sleep(1)
    await client.send_reaction(chat_id=chat, message_id=id, emoji=random_emoji)
    
    
@USU.BOT("control")
@USU.DEVS
async def _(client, message):
    buttons = BTN.BOT_HELP(message)
    sh = await message.reply(f"<b><i>Help Menu Information</i></b>", reply_markup=InlineKeyboardMarkup(buttons))
    

@USU.CALLBACK("balik")
async def _(client, callback_query):
    buttons = BTN.BOT_HELP(callback_query)
    sh = await callback_query.message.edit(f"<b><i>Help Menu Information</b></i>", reply_markup=InlineKeyboardMarkup(buttons))


@USU.CALLBACK("reboot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer("Tombol ini bukan untuk anda!", show_alert=True)
    await callback_query.answer("System restarted!", show_alert=True)
    os.system(f"kill -9 {os.getpid()} && bash start.sh")


@USU.CALLBACK("update")
async def _(client, callback_query):
    out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer("Tombol ini bukan untuk anda!", show_alert=True)
    if "Already up to date." in str(out):
        return await callback_query.answer("Sudah versi terbaru!", show_alert=True)
    else:
        await callback_query.answer("Processing!", show_alert=True)
    os.system(f"kill -9 {os.getpid()} && bash start.sh")

@USU.CALLBACK("shutdown")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer("Tombol ini bukan untuk anda!", show_alert=True)
    await callback_query.answer("System is shutdown!", show_alert=True)
    os.system(f"kill -9 {os.getpid()}")


@USU.CALLBACK("statss")
async def _(client, callback_query):
    await callback_query.answer("Refresh")
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = round((end - start).microseconds / 1000)
    delta_ping_formatted = round(delta_ping, 3)
    uptime = await get_time((time() - start_time))
    alive = await usu_alive()
    _ping = f"""
<b><i>Information System!</i></b>
   <i><b>Pong:</b> {str(delta_ping)} ms</i>
   <i><b>Alive:</b></i> {alive}
   <i><b>Client:</b> {len(ubot._ubot)}</i>
"""
    buttons = [[InlineKeyboardButton("Refresh", callback_data="statss"), InlineKeyboardButton("Back", callback_data="balik")]]
    try:
        await callback_query.message.edit(_ping, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        return


@USU.CALLBACK("system")
async def _(client, callback_query):
    await callback_query.answer("Refresh")
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    _ping = f"""
<i><b>Information System!
   <i><b>Cpu:</b> {cpu}%</i>
   <i><b>Ram:</b> {mem}%</i>
   <i><b>Disk:</b> {disk}%</i>
   <i><b>Memory:</b> {round(process.memory_info()[0] / 1024 ** 2)} mb</i>
"""
    buttons = [[InlineKeyboardButton("Refresh", callback_data="system"), InlineKeyboardButton("Back", callback_data="balik")]]
    try:
        await callback_query.message.edit(_ping, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        return
