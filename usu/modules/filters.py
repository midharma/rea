import random
import re

from pyrogram import filters, Client
from asyncio import sleep
from re import search, IGNORECASE, escape


from usu import *

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from re import findall

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions




@USU.NO_CMD("FILTERS_GC", ubot)
async def _(client, message):
    try:
        all_filters = await db.all_vars(client.me.id, "FILTERS_GC") or {}

        for key, value in all_filters.items():
            if key in message.text.lower().split():
                return await message.reply(value)
    except BaseException:
        pass






@USU.UBOT("filter")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    txt = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    arg = get_arg(message)

    if not arg or arg.lower() not in ["off", "on"]:
        return await txt.edit(f"<i><b>Type [on/off]</b></i>")

    type = True if arg.lower() == "on" else False
    await db.set_vars(client.me.id, "FILTERS_GC_ON_OFF", type)
    return await txt.edit(f"<i><b>{sks}Successfully set to mode: {type}</b></i>")


@USU.UBOT("addfilter")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    txt = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    type, reply = extract_type_and_msg(message)

    all = await db.all_vars(client.me.id, "FILTERS_GC") or {}
    if not type and message.reply_to_message:
        return await txt.edit(f"<i><b>{ggl}Reply text or enter text</b></i>")
    if type not in all:
        try:
            await db.set_vars(client.me.id, type, str(reply.text), "FILTERS_GC")
            await txt.edit(f"<i><b>{sks}Message:</b> <code>{type}</code> <b>Successfully added to filter</b></i>")
        except Exception as error:
            await txt.edit(error)
    else:
        return await txt.edit(f"<i><b>{ggl}Cannot create new a filter</b></i>")


@USU.UBOT("delfilter")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    txt = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    arg = get_arg(message)

    if not arg:
        return await txt.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>nama filter</b></i>")

    logs = bot.me.id
    all = await db.all_vars(client.me.id, "FILTERS_GC") or {}

    if arg not in all:
        return await txt.edit(f"<i><b>{ggl}Message:</b> <code>{arg}</code> <b>Not found!</b></i>")

    await db.remove_vars(client.me.id, arg, "FILTERS_GC")
    return await txt.edit(f"<i><b>{sks}Message:</b> <code>{arg}</code> <b>Successfully removed to filter</b></i>")


@USU.UBOT("clearfilter")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    txt = await message.reply(f"<i><b>{prs}Processing...</b></i>")

    all = await db.all_vars(client.me.id, "FILTERS_GC")
    for anu in all:
        await db.remove_vars(client.me.id, anu, "FILTERS_GC")
    return await txt.edit(f"<i><b>{sks}Successfully removed all filter</b></i>")

@USU.UBOT("filters")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    all_filters = await db.all_vars(client.me.id, "FILTERS_GC")
    if all_filters:
        msg = f"{broad}List filters\n"
        for x in all_filters.keys():
            msg += f"{x}\n"
        msg += f"{sks}Total filters: {len(all_filters)}"
    else:
        msg = f"<b>{ggl}Filters not found!</b>"

    await message.reply(f"<i>{msg}</i>", quote=True)




