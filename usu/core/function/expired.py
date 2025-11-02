import asyncio
from datetime import datetime

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytz import timezone

from usu import *
from usu.core.helpers.text import MSG
from urllib.parse import quote


async def send_to_user(client, day):
    hazmi = "Halo! saya ingin perpanjang Userbot"
    url = f"https://t.me/{USERNAME}?text={quote(hazmi)}"
    btn = [[InlineKeyboardButton("Owners", url=url)]]
    try:
        await bot.send_message(
            client.me.id,
            MSG.EXP_SISA(client, day),
            reply_markup=InlineKeyboardMarkup(btn),
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await bot.send_message(
            client.me.id,
            MSG.EXP_SISA(client, day),
            reply_markup=InlineKeyboardMarkup(btn),
        )
    except Exception:
        pass


async def send_to_devs(client, day):
    user_link = f"{client.me.first_name} {client.me.last_name or ''}"
    gbt = [[InlineKeyboardButton(user_link, url=f"tg://openmessage?user_id={client.me.id}")]]
    for dev_id in DEVS:
        try:
            await bot.send_message(
                dev_id,
                f"<i><b>Information Userbot!\nName:</b> {client.me.mention}"
                f"\n<b>ID:</b> <code>{client.me.id}</code>"
                f"\n<b>Expired:</b> tersisa {day} hari</i>",
                reply_markup=InlineKeyboardMarkup(gbt),
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await bot.send_message(
                dev_id,
                f"<i><b>Information Userbot!\nName:</b> {client.me.mention}"
                f"\n<b>ID:</b> <code>{client.me.id}</code>"
                f"\n<b>Expired:</b> tersisa {day} hari</i>",
                reply_markup=InlineKeyboardMarkup(gbt),
            )
        except Exception:
            pass


async def expiredUserbots():
    while True:
        await asyncio.sleep(120)
        for X in tuple(ubot._ubot.values()):
            try:
                time_now = datetime.now(pytz.timezone("Asia/Jakarta"))
                exp_datetime = await db.get_expired_date(X.me.id)

                if exp_datetime is None:
                    continue

                day = (exp_datetime - time_now).days

                if time_now > exp_datetime:
                    try:
                        await X.unblock_user(bot.me.username)
                    except Exception:
                        pass
                    await send_to_user(X, day)
                    await send_to_devs(X, day)

                    await db.remove_ubot(X.me.id)
                    await db.remove_all_vars(X.me.id)
                    await db.rem_expired_date(X.me.id)

                    logger.info(f"Client - {X.me.id} - Masa aktif telah habis!")
                    await X.log_out()
                    del ubot._ubot[X.me.id]

                elif day in (7, 3) and abs((time_now - exp_datetime.replace(year=time_now.year, month=time_now.month, day=time_now.day)).total_seconds()) <= 60:
                    await send_to_user(X, day)
                    await send_to_devs(X, day)
                    logger.info(f"Client - {X.me.id} - Masa aktif tersisa {day} hari!")

            except Exception as e:
                if X.me.id not in DEVS:
                    logger.error(f"Error {e}")