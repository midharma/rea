from usu import *
from usu import config
import random
import requests
import asyncio
import os
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message
from MukeshAPI import api
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired, MessageIdInvalid, MessageDeleteForbidden
from usu.core.helpers.tools import process_ai, waktu_tunggu

import re
import time
from datetime import datetime, timedelta

from pathlib import Path
from urllib.parse import urlparse

from pyrogram.enums import ChatMemberStatus



@USU.CALLBACK("^chatbot")
async def _(c, cq):
    button = BTN.TAMBAH()
    pesan = f"""<i><b>Halo,
Saya adalah menu [ChatBot-AI]({PHOTO})

Command Admins:</b>
/chatbot - on/off</i>

<b>Catatan:</b>
<i>Fitur ini bekerja ketika bot nya telah jadi admin di group</i>
<i>Jika fitur /chatbot on, maka otomatis akan menonaktifkan fitur /ankes</i>"""
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))






@USU.NO_CMD("CHATAI", bot)
async def chat_ai(client, message: Message):
    if not GEMINI_KEY:
        return
    if message.text.startswith("/"):
        return

    admins = await list_admins(client, message.chat.id)
    if message.from_user.id in admins or bot.me.id not in admins:
        return
    if message.reply_to_message and message.reply_to_message.from_user.id != bot.me.id:
        return

    can_process = await waktu_tunggu(client, message.chat.id)
    if not can_process:
        return

    await process_ai(client, message)


@USU.BOT("chatbot")
@USU.GROUP
@USU.ADMIN
async def togel_ai(client, message):
    if not GEMINI_KEY:
        return await message.reply(f"<b><i>Fitur ini lagi maintenance!</i></b>")
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(message.chat.id, "AI_ON_OFF")
    group = await db.get_list_from_vars(bot.me.id, "group")
    if message.chat.id not in group:
        if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            await db.add_to_vars(bot.me.id, "group", message.chat.id)
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>`"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    if command == "on":
        if not vars:
            await db.set_vars(message.chat.id, "AI_ON_OFF", query[command])
            await db.set_vars(message.chat.id, "ON_OFF_WORD", False)
            return await message.reply(f"<i><b>{sks}Chatbot on!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Chatbot sudah on sebelumnya!</b></i>")
    else:
        if vars:
            await db.set_vars(message.chat.id, "AI_ON_OFF", query[command])
            return await message.reply(f"<i><b>{sks}Chatbot off!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Chatbot sudah off sebelumnya!</b></i>")


#===============


@USU.UBOT("chatbot")
@USU.GROUP
async def togel_ai_client(client, message):
    if not GEMINI_KEY:
        return await message.reply(f"<b><i>Fitur ini lagi maintenance!</i></b>")
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_list_from_vars(client.me.id, "CLIENT_AI_ON_OFF")
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>`"
        )

    query = ["on", "off"]
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    if command == "on":
        if message.chat.id not in vars:
            await db.add_to_vars(client.me.id, "CLIENT_AI_ON_OFF", message.chat.id)
            return await message.reply(f"<i><b>{sks}Chatbot on!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Chatbot sudah on sebelumnya!</b></i>")
    else:
        if message.chat.id in vars:
            await db.remove_from_vars(client.me.id, "CLIENT_AI_ON_OFF", message.chat.id)
            return await message.reply(f"<i><b>{sks}Chatbot off!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Chatbot sudah off sebelumnya!</b></i>")


@USU.UBOT("listchatbot")
async def list_chatbot(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)

    vars = await db.get_list_from_vars(client.me.id, "CLIENT_AI_ON_OFF")

    if not vars:
        return await message.reply(f"<b><i>{ggl} Belum ada grup yang mengaktifkan chatbot.</i></b>")

    teks = f"<b>📜 Daftar Grup dengan Chatbot ON:</b>\n"
    for i, gc_id in enumerate(vars, 1):
        try:
            chat = await client.get_chat(gc_id)
            teks += f"{i}. {chat.title or chat.first_name} <code>({gc_id})</code>\n"
        except:
            teks += f"{i}. [Tidak bisa resolve] <code>({gc_id})</code>\n"

    return await message.reply(teks)

@USU.UBOT("clearchatbot")
async def clear_all_chatbot(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)

    vars = await db.get_list_from_vars(client.me.id, "CLIENT_AI_ON_OFF")
    if not vars:
        return await message.reply(f"<b><i>{ggl} Tidak ada data chatbot yang aktif.</i></b>")

    # hapus semua data
    for gc_id in vars:
        await db.remove_from_vars(client.me.id, "CLIENT_AI_ON_OFF", gc_id)

    return await message.reply(f"<i><b>{sks}Berhasil menghapus semua daftar grup chatbot.</b></i>")



@USU.NO_CMD("CHATAI_CLIENT", ubot)
async def chat_ai_client(client, message: Message):
    if not GEMINI_KEY:
        return

    admins = await list_admins(client, message.chat.id)
    if message.from_user.id in admins or client.me.id not in admins:
        return
    if message.reply_to_message and message.reply_to_message.from_user.id != client.me.id:
        return
    can_process = await waktu_tunggu(client, message.chat.id)
    if not can_process:
        return
    await process_ai(client, message)