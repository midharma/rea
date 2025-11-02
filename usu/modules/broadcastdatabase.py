import asyncio
import random

import os
import json
import asyncio
import psutil

from pyrogram.raw import *
from pyrogram import Client

from gc import get_objects
from pyrogram.raw.functions.messages import DeleteHistory, StartBot

from pyrogram.errors.exceptions import FloodWait

from usu import *



@USU.UBOT("addbcdb")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"
    msg = await message.reply(_msg)
    if len(message.command) > 1:
        gc = message.command[1]
    else:
        gc = message.chat.id
    try:
        chat_id = await extract_id(message, gc)
        bcdb = await db.get_list_from_vars(client.me.id, "bcdb")
        if not chat_id:
            return await msg.edit(f"""<i><b>{ggl}Invalid!</b></i>""")
        if chat_id in blacklist:
            return await msg.edit(f"""<i><b>{ggl}Already in the broadcast database!</b></i>""")
        await db.add_to_vars(client.me.id, "bcdb", chat_id)
        return await msg.edit(f"""<i><b>{sks}Added to broadcast database!</b></i>""")
    except Exception as error:
        return await msg.edit(str(error))


@USU.UBOT("unbcdb")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"
    msg = await message.reply(_msg)
    if len(message.command) > 1:
        gc = message.command[1]
    else:
        gc = message.chat.id
    try:
        chat_id = await extract_id(message, gc)
        bcdb = await db.get_list_from_vars(client.me.id, "bcdb")

        if chat_id not in bcdb:
            response = f"""<i><b>{ggl}Not in broadcast database!</b></i>
"""
        else:
            await db.remove_from_vars(client.me.id, "bcdb", chat_id)
            response = f"""<i><b>{sks}Remove broadcast database!</b></i>
"""

        return await msg.edit(response)
    except Exception as error:
        return await msg.edit(str(error))


@USU.UBOT("listbcdb")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"
    mzg = await message.reply(_msg)

    bcdb = await db.get_list_from_vars(client.me.id, "bcdb")
    total_bcdb = len(bcdb)
    if not bcdb:
        return await mzg.edit(f"<i><b>{ggl}Empty!</b></i>")

    list_text = f"{broad}Daftar database broadcast!\n\n"

    for chat_id in bcdb:
        try:
            chat = await client.get_chat(chat_id)
            list_text += f"{chat.title} | {chat.id}\n"
        except:
            pass

    list_text += f"{sks}Total broadcast database {total_bcdb}"
    return await mzg.edit(f"<i><b>{list_text}</b></i>")


@USU.UBOT("clearbcdb")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"

    msg = await message.reply(_msg)
    bcdb = await db.get_list_from_vars(client.me.id, "bcdb")

    if not bcdb:
        return await msg.edit(f"<i><b>{ggl}Empty!</b></i>")

    for chat_id in bcdb:
        await db.remove_from_vars(client.me.id, "bcdb", chat_id)

    await msg.edit(f"<i><b>{sks}Clear broadcast database!</b></i>")