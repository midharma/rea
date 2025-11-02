import asyncio
import random
from random import shuffle
from pyrogram import idle
from usu import *
from usu.modules import loadModule
from usu.core.helpers.help_usu import tombol_anak
from usu.core.database.local import db
from usu.core.helpers.dec import installPeer
import os
import aiorun
import traceback
import sys

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered, SessionRevoked, UserAlreadyParticipant, UserNotParticipant, UserDeactivated, UserDeactivatedBan, FloodWait)
import pytgcalls
import pyrogram
import time
import shutil
import pytz
from datetime import datetime

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from usu.core.helpers.inline import BTN

tagall_task = {}
tagallgcid = {}
pesan = {}

async def autotagall_loop():
    global tagallgcid
    if bot.me.id not in tagallgcid:
        tagallgcid[bot.me.id] = []
    while True:
        await asyncio.sleep(30)
        vars = await db.get_list_from_vars(bot.me.id, "auto_tagall")
        if vars:
            try:
                now = datetime.now(pytz.timezone("Asia/Jakarta")).strftime("%H:%M")
                for target in vars:
                    chat_id = target["chat_id"]
                    for isi in target["data"]:
                        if now == isi["jam"]:
                            if chat_id not in tagallgcid[bot.me.id]:
                                tagallgcid[bot.me.id].append(chat_id)
                                asyncio.create_task(run_tagall(chat_id, isi["pesan"], durasi=300))
                                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"[autotagall_loop] error: {e}")



async def run_tagall(chat_id, text, durasi):
    global tagallgcid, pesan
    try:
        end_time = time.time() + durasi
        if chat_id not in pesan:
            pesan[chat_id] = []
        if bot.me.id not in tagallgcid:
            tagallgcid[bot.me.id] = []
        while time.time() < end_time:
            users = []
            async for member in bot.get_chat_members(chat_id):
                if not (member.user.is_bot or member.user.is_deleted):
                    if chat_id not in tagallgcid[bot.me.id]:
                        break
                    nama = f"{member.user.first_name} {member.user.last_name or ''}".strip()
                    targetnya = f"<a href=tg://user?id={member.user.id}>{nama}</a>"
                    users.append(targetnya)
                    if len(users) == 5:
                        shuffle(users)
                        anu = ", ".join(users)
                        try:
                            await asyncio.sleep(2)
                            msg = await bot.send_message(chat_id, f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN()))
                            pesan[chat_id].append(msg.id)
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            await asyncio.sleep(2)
                            msg = await bot.send_message(chat_id, f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN()))
                            pesan[chat_id].append(msg.id)
                        users = []
            if users:
                shuffle(users)
                anu = ", ".join(users)
                try:
                    await asyncio.sleep(2)
                    msg = await bot.send_message(chat_id, f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN()))
                    pesan[chat_id].append(msg.id)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await asyncio.sleep(2)
                    msg = await bot.send_message(chat_id, f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN()))
                    pesan[chat_id].append(msg.id)
            break
        try:
            tagallgcid[bot.me.id].remove(chat_id)
        except Exception:
            pass
        if chat_id in pesan:
            await asyncio.sleep(60)
            try:
                for msg_id in pesan[chat_id]:
                    await bot.delete_messages(chat_id, msg_id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                for msg_id in pesan[chat_id]:
                    await bot.delete_messages(chat_id, msg_id)
            except Exception:
                for msg_id in pesan[chat_id]:
                    await bot.delete_messages(chat_id, msg_id)
    except Exception as e:
        logger.error(str(e))