import os
import json
import asyncio
import psutil


from datetime import datetime
from gc import get_objects
from time import time

from pyrogram.raw import *
from pyrogram import Client
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from usu import *

@USU.UBOT("ping|p")
@ubot.on_message(filters.command("cping|cp", "") & filters.user(DEVS))
async def pingbro(client, message):
    vars = await db.get_vars(client.me.id, "switch")
    if vars:
        return await pingu(client, message)
    else:
        return await pingme(client, message)

@USU.BOT("ping")
async def pingbro(client, message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping)
    alive = await usu_alive()
    _ping = f"""
<b><i>Pong..!!</i></b>\n<code>{delta_ping} ms</code>
<i><b>Bot Hidup:</b></i> {alive}
"""
    await message.reply_text(_ping)



async def pingme(client, message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping)
    _ping = f"""
<b><i>Pong..!!</i></b>\n<code>{delta_ping} ms</code>
"""
    await message.reply_text(_ping)


async def pingu(client, message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping)
    uptime = await get_time((time() - start_time))
    up = await EMO.UPTIME(client)
    pong = await EMO.PING(client)
    tion = await EMO.MENTION(client)
    upt = await TEXT.UPTIME(client)
    ping = await TEXT.PING(client)
    mention = await TEXT.MENTION(client)
    alive = await usu_alive()
    _ping = f"""
<i><b>{pong}{ping}</b> {str(delta_ping)} ms</i>
<i><b>{tion}{mention}</b> {client.me.mention}</i>
<i><b>{up}{upt}</b></i> {alive}
"""
    await message.reply(_ping)
