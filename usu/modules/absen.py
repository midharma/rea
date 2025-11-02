from pyrogram import Client, filters
from pyrogram.types import (InlineKeyboardMarkup, InlineQueryResultArticle,                            InputTextMessageContent, InlineKeyboardButton)
from datetime import datetime
import pytz

from usu import *


hadir_list = []

def get_hadir_list(client):
    return "\n".join([f"{no+1}. {user['mention']} - {user['jam']}" for no, user in enumerate(hadir_list)])

@USU.UBOT("clearabsen")
async def clear_absen_command(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if not hadir_list:
        await message.reply(f"<b><i>{ggl}Not absen!</i></b>")
    else:
        hadir_list.clear()
        await message.reply(f"<b>{sks}Clear absen!</b>")

@USU.INLINE("^absen_in")
async def absen_query(client, inline_query):
    user_id = inline_query.from_user.id
    mention = inline_query.from_user.mention
    timestamp = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%d %B %Y")
    jam = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%H.%M.%S")

    hadir_text = get_hadir_list(client)

    text = f"<b>Tanggal:\n{timestamp}\n\nDaftar:\n{hadir_text}\n\n</b>"
    buttons = [[InlineKeyboardButton("Absen", callback_data="absen_hadir")]]
    keyboard = InlineKeyboardMarkup(buttons)
    results = [
        (
            InlineQueryResultArticle(
                title="💬",
                input_message_content=InputTextMessageContent(text),
                reply_markup=keyboard
            )
        )
    ]
    await inline_query.answer(results=results)


@USU.CALLBACK("absen_hadir")
async def hadir_callback(client, callback_query):
    user_id = callback_query.from_user.id
    mention = callback_query.from_user.mention
    timestamp = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%d %B %Y")
    jam = datetime.now(pytz.timezone('asia/Jakarta')).strftime("%H.%M.%S")
    if any(user['user_id'] == user_id for user in hadir_list):
        await callback_query.answer("Anda sudah absen sebelumnya!", show_alert=True)
    else:
        hadir_list.append({"user_id": user_id, "mention": mention, "jam": jam})
        hadir_text = get_hadir_list(client)
        text = f"<b>Tanggal:\n{timestamp}\n\nDaftar:\n{hadir_text}\n\n</b>"
        buttons = [[InlineKeyboardButton("Absen", callback_data="absen_hadir")]]
        keyboard = InlineKeyboardMarkup(buttons)
        await callback_query.edit_message_text(text, reply_markup=keyboard)


@USU.UBOT("absen")
async def absen_command(client, message):
    try:
        x = await client.get_inline_bot_results(bot.me.username, "absen_in")
        if x.results:
            await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        else:
            await message.reply(f"<b><i>Error!</i></b>")
    except asyncio.TimeoutError:
        await message.reply(f"<b><i>Error!</i></b>")
    except Exception as e:
        await message.reply(e)