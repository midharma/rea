from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatType

from usu.config import OWNER_ID, PHOTO, USERNAME
from usu import OWNER_ID, bot, db, ubot
from usu import *
from usu.core.helpers.uptime import *


class MSG:
    async def MEMBER():
        usu_time = await usu_alive()
        return f"""<b><i>Halo,
Saya adalah [{bot.me.first_name}]({PHOTO})..!!

Silahkan adminkan Bot ini di group anda dengan akses penuh!

Bot Hidup:</i></b>
{usu_time}
"""

    def EXP_MSG_UBOT(X):
        return f"""<i><b>Information Userbot!</b>
<b>Name:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>ID:</b> {X.me.id}
<b>Catatan:</b>
Userbot anda telah habis! Perpanjang?PM Contact di bawah ini!</i>
"""

    def EXP_SISA(X, day):
        return f"""<i><b>Information Userbot!</b>
<b>Name:</b> <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a>
<b>ID:</b> {X.me.id}
<b>Catatan:</b>
Userbot anda tersisa {day} hari! Perpanjang?PM Contact di bawah ini!</i>
"""

    async def PILIHAN():
        usu_time = await usu_alive()
        group_list = await db.get_list_from_vars(bot.me.id, "group") or []
        channel_list = await db.get_list_from_vars(bot.me.id, "channel") or []
        group = len(group_list)
        channel = len(channel_list)
        terjual = await db.get_vars(bot.me.id, "penjualan") or 0
        return f"""<b><i>Halo,
Saya adalah [{bot.me.first_name}]({PHOTO})..!!

Bot Hidup:</i></b>
{usu_time}

<i><b>Koneksi Group & Channel:</b>
{group} & {channel}</i>

<i><b>Privasi & Keamanan:</b>
Seluruh data dalam sistem ini disimpan secara aman menggunakan metode enkripsi tingkat tinggi. Informasi sensitif di dalam database tidak dapat diakses atau dibaca tanpa otorisasi yang sah.</i>

<i><b>Terjual:</b>
{terjual}</i>

<i><b>{bot.device_model}</b>
Version {bot.app_version}</i>
"""

    async def START():
        return f"""<b><i>Halo,
Anda sekarang berada di menu [Userbot]({PHOTO})..!!</i></b>
"""


    async def UBOT(count):
        return f"""<i><b>Userbot To</b> <code>{int(count) + 1}/{len(ubot._ubot)}</code>
<b>Account:</b> <a href=tg://user?id={ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.id}>{ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.first_name} {ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.last_name or ''}</a> 
<b>ID:</b> <code>{ubot._ubot[tuple(ubot._ubot.keys())[int(count)]].me.id}</code></i>
"""