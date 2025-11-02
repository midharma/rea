import asyncio
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone
from pyrogram.errors import AuthKeyUnregistered, SessionRevoked, RPCError, InputUserDeactivated
from pyrogram.types import InlineKeyboardMarkup
from pyrogram import Client, errors
import pyrogram
from pyrogram.raw.functions.auth import LogOut
from usu import *

"""async def check_session():
    while True:
        await asyncio.sleep(120)
        for usu in list(ubot._ubot.values()):
            try:
                await usu.get_me()
            except (AuthKeyUnregistered, SessionRevoked, InputUserDeactivated) as e:
                user_id = getattr(usu.me, "id", None)
                try:
                    if usu.me and not usu.me.is_deleted:
                        await bot.send_message(
                            usu.me.id,
                            "<b><i>Sesi userbot Anda telah terlepas.\nSilahkan install ulang userbot anda kembali.</i></b>"
                        )
                except Exception:
                    pass

                try:
                    if user_id:
                        await db.remove_ubot(user_id)
                        akses_list = await db.get_list_from_vars(bot.me.id, "AKSES")
                        if user_id not in akses_list:
                            await db.add_to_vars(bot.me.id, "AKSES", user_id)
                except Exception as db_err:
                    logger.error(f"[DB ERROR] - {usu.me.id}: {db_err}")

                try:
                    await usu.log_out()
                except Exception as e:
                    logger.error(f"[LOGOUT FAILED] - {usu.me.id}: {e}")
                try:
                    if user_id:
                        del ubot._ubot[user_id]
                except Exception:
                    pass

            except Exception as e:
                logger.error(f"[UNKNOWN ERROR] - {usu.me.id}: {e}")"""


async def check_session():
    while True:
        await asyncio.sleep(120)
        for usu in list(ubot._ubot.values()):
            try:
                await usu.get_me()
            except (AuthKeyUnregistered, RPCError) as e:
                try:
                    user_id = getattr(usu.me, "id", None)
                    if not user_id:
                        continue
                    user = await bot.get_users(user_id)
                    if not user.is_deleted:
                        await bot.send_message(user_id, f"<b><i>Sesi userbot anda terlepas, silahkan membuat userbot kembali!</i></b>")
                except Exception as e:
                    pass
                await db.remove_ubot(user_id)
                if user_id not in await db.get_list_from_vars(bot.me.id, "AKSES"):
                    await db.add_to_vars(bot.me.id, "AKSES", user_id)
                await usu.invoke(LogOut())
                del ubot._ubot[user_id]
            except OSError as e:
                pass
            except Exception as e:
                logger.error(f"Session error: {e}")