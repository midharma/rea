from usu import *
from pyrogram.raw import functions
from pyrogram import filters
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import CallbackQuery
from pyrogram.enums import ParseMode
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
import asyncio
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong



@USU.CALLBACK("^jawab_pesan")
async def gendeng_jing(client, callback_query: CallbackQuery):
    user_id = int(callback_query.from_user.id)
    user_ids = int(callback_query.data.split()[1])
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    if user_ids == OWNER_ID:
        try:
            pesan = await client.ask(
                user_id,
                f"<b><i>Silahkan kirim balasan anda!</i></b>",
                timeout=60,
            )
            await client.send_message(
                user_id,
                f"<b><i>Pesan anda sudah terkirim, mohon tunggu balasannya!</i></b>",
            )
            await callback_query.message.delete()
        except asyncio.TimeoutError:
            return await client.send_message(user_id, f"<b><i>Pembatalkan otomatis!</i></b>")
        buttons = [
            [
                IKB(full_name, callback_data=f"profil {user_id}"),
            ],
            [
                IKB("Balas Pesan", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
        await pesan.copy(
            user_ids,
            reply_markup=IKM(buttons),
        )
    else:
        if user_id != OWNER_ID:
            return await callback_query.answer("Tombol ini khusus Owner", True)
        try:
            buttons = [
                [
                    IKB("Balas Pesan", callback_data=f"jawab_pesan {OWNER_ID}"),
                ],
            ]
            pesan = await client.ask(
                OWNER_ID,
                f"<b><i>Silahkan kirim balasan anda!</i></b>",
                timeout=60,
            )
            await client.send_message(
                OWNER_ID,
                f"<b><i>Pesan anda sudah terkirim!</i></b>",
            )
        except asyncio.TimeoutError:
            await client.send_message(OWNER_ID, f"<b><i>Pembatalkan otomatis!</i></b>")

        await pesan.copy(
            user_ids,
            reply_markup=IKM(buttons),
        )