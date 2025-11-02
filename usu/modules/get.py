import asyncio

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from usu import *



@USU.CALLBACK("^profil")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    try:
        get = await bot.get_users(user_id)
        first_name = f"{get.first_name}"
        last_name = f"{get.last_name}"
        full_name = f"{get.first_name} {get.last_name or ''}"
        username = f"{get.username}"
        msg = (
            f"<b>Mention: <a href=tg://user?id={get.id}>{full_name}</a></b>\n"
            f"<b>ID-Pengguna:</b> <code>{get.id}</code>\n"
            f"<b>Nama Depan:</b> {first_name}\n"
        )
        if last_name == "None":
            msg += ""
        else:
            msg += f"<b>Nama Belakang:</b> {last_name}\n"
        if username == "None":
            msg += ""
        else:
            msg += f"<b>Username:</b> @{username}\n"
        msg += f"<b>Bot: {bot.me.mention}\n"
        buttons = [
            [
                InlineKeyboardButton(
                    f"{full_name}",
                    url=f"tg://openmessage?user_id={get.id}",
                )
            ]
        ]
        await callback_query.message.reply_text(
            f"<i>{msg}</i>", reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as why:
        await callback_query.message.reply_text(why)
