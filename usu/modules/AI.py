from usu import *
from usu import config
import random
import requests
import asyncio
import random
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message
from MukeshAPI import api
from pyrogram import filters
import inspect
from pyrogram.errors import ChatAdminRequired
import re
from datetime import datetime, timedelta
from usu.core.helpers.tools import process_ai_ask

@USU.UBOT("ask|ai|gemini")
async def ask_handler(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prss = await EMO.PROSES(client)
    if not GEMINI_KEY:
        return await message.reply(f"<i><b>{ggl}Fitur ini maintenance!</b></i>")
    # Kirim pesan proses
    prs = await message.reply(f"<i><b>{prss}Processing...</b></i>")

    # Ambil input user
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    elif len(message.command) > 1:
        user_input = " ".join(message.command[1:])
    else:
        await prs.edit(f"<i><b>{ggl} {message.text} berikan sesuatu untuk dijawab</b></i>")
        return

    # Simulasi typing sebentar sebelum panggil AI
    await asyncio.sleep(random.uniform(0.3, 0.8))

    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        await prs.delete()
        # Panggil get_ai_response
        await process_ai_ask(client, message)
    except Exception as e:
        await message.reply(f"<i><b>{ggl} Terjadi error: {e}</b></i>")

