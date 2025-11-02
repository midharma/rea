import random
import re

from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import *
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from usu.config import OWNER_ID

from usu import *

@USU.UBOT("alive")
async def _(client, message):
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"alive {client.me.id}"
        )
        await message.reply_inline_bot_result(x.query_id, x.results[0].id, quote=True)
    except Exception as error:
        await message.reply(error)




@USU.INLINE("^alive")
async def _(client, inline_query):
    get_id = inline_query.query.split()
    button = BTN.ALIVE()
    for my in ubot._ubot.values():
        if int(get_id[1]) == my.me.id:
            try:
                peer = my.peer[my.me.id]
                users = len(peer["pm"])
                group = len(peer["gc"])
            except Exception:
                users = random.randrange(await my.get_dialogs_count())
                group = random.randrange(await my.get_dialogs_count())
            get_exp = await db.get_expired_date(my.me.id)
            exp = get_exp.strftime("%d %B %Y") if get_exp else "None"
            if my.me.id in DEVS:
                status = f"<i>Active! [Owner]</i>"
            elif my.me.id in await db.get_list_from_vars(client.me.id, "SELER_USERS") and my.me.id not in DEVS:
                status = f"<i>Active! [Seller]</i>"
            else:
                status = f"<i>Active!</i>"
            start = datetime.now()
            await my.invoke(Ping(ping_id=0))
            ping = (datetime.now() - start).microseconds / 1000
            uptime = await get_time((time() - start_time))
            time_usu = await usu_alive()
            msg = f"""<b><i>{bot.me.first_name}</i></b>
  <b><i>• Status:</i></b> {status} 
    <b><i>• Expired:</i></b> <i>{exp}</i>
    <b><i>• Name:</i></b> <i>{my.me.mention}</i>
    <b><i>• ID:</i></b> <i>{my.me.id}</i>
    <b><i>• Peer-User:</i></b> <i>{users}</i>
    <b><i>• Peer-Group:</i></b> <i>{group}</i>
    <b><i>• Alive:</i></b> {time_usu}
"""
            results = [
                (
                    InlineQueryResultArticle(
                        title="💬",
                        reply_markup=InlineKeyboardMarkup(button),
                        input_message_content=InputTextMessageContent(msg),
                    )
                )
            ]
            await inline_query.answer(results=results)


@USU.CALLBACK("alv_cls")
async def _(client, callback_query):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    delta_ping = (end - start).microseconds / 1000
    delta_ping_formatted = round(delta_ping)
    return await callback_query.answer(f"{delta_ping} ms", show_alert=True)