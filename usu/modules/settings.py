from usu import *

from pyrogram.raw import *
from pyrogram import Client
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import json
import requests





@USU.UBOT("sp")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Tm = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) < 2:
        return await Tm.edit(f"<i>{ggl}<code>{message.text}</code> <b>[simbol]</b></i>")
    else:
        ub_prefix = []
        for prefix in message.command[1:]:
            if prefix.lower() == "none":
                ub_prefix.append("")
            else:
                ub_prefix.append(prefix)
        try:
            client.set_prefix(message.from_user.id, ub_prefix)
            await db.set_pref(message.from_user.id, ub_prefix)
            parsed_prefix = " ".join(f"<code>{prefix}</code>" for prefix in ub_prefix)
            return await Tm.edit(f"<i><b>{sks}Prefix successfully changed!</b></i>")
        except Exception as error:
            return await Tm.edit(str(error))


"""@USU.UBOT("2fa")
async def ganti_twofa(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    args = message.text.split()
    if len(args) != 3:
        await message.reply(f"<b><i>{ggl}Masukkan old password dan new password!</i></b>")
        return
    old_password = args[1]
    new_password = args[2]
    try:
        await client.change_cloud_password(old_password, new_password)
        await db.set_two_factor(message.from_user.id, new_password)
        await message.reply(f"<b><i>{sks}Two-factor authentication berhasil diganti!</i></b>")
    except Exception as e:
        await message.reply(f"<b><i>{ggl}Gagal mengganti two-factor authentication: {e}</i></b>")
"""