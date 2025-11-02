

import asyncio
import time
from datetime import datetime

import speedtest

from pyrogram.raw.functions import Ping
from pyrogram.raw import functions
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from usu import *



@USU.UBOT("stats")
async def stats(client, message):
    prs = await EMO.PROSES(client)
    usu = await message.reply_text(f"<b><i>{prs}Processing...</i></b>")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    usi = await client.get_me()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type == enums.ChatType.GROUP:
            g += 1
            user_s = await dialog.chat.get_member(int(usi.id))
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(usi.id))
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await usu.edit_text(
        """<i><b>Information!
Ping {} ms
Private Message {} 
Group {}
Super Group {}
Admin Group {}
Bot = {}</b></i>""".format(
            ms, u, g, sg, c, a_chat, b
        )
    )




