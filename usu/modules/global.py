import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.errors import FloodWait

from usu import *


GKICK = """Command for <b>Global Kicked</b>

<b>Global kick</b>
 <i>kick user dari semua group chat</i> 
    <code>{0}gkick</code> [username]"""


GMUTE = """Command for <b>Global Muted</b>

<b>Global mute</b>
 <i>mute user dari semua group chat</i> 
    <code>{0}gmute</code> [username]
 <i>unmute user dari semua group chat</i>
    <code>{0}ungmute</code> [usename]"""


GBAN = """Command for <b>Global Banned</b>

<b>Global ban</b>
 <i>banned user dari semua group chat</i> 
    <code>{0}gban</code> [username]
 <i>unbanned user dari semua group chat</i>
    <code>{0}ungban</code> [usename]"""


__UTAMA__ = "Globals"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Gmute", "Gban", "Gkick"

__HASIL__ = GMUTE, GBAN, GKICK



@USU.UBOT("gmute")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    _msg = f"<i><b>{prs}Processing...</b></i>"

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        if user.id == client.me.id:
            return await Tm.edit(f"<i><b>{ggl}Anda tidak bisa gmute diri sendiri!</b><i>")
        if user.id in DEVS:
            return await Tm.edit(f"<i><b>{ggl}Anda tidak bisa gmute dia karena dia pemilik bot ini!</b><i>")
        try:
            await client.restrict_chat_member(dialog, user.id, ChatPermissions())
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.restrict_chat_member(dialog, user.id, ChatPermissions())
                done += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1
    text = f"""<i><b>{broad}Global Muted!
{sks}Success: {done} chats
{ggl}Failed: {failed} chats
{ptr}User: <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a></b></i>"""
    await message.reply(text)
    return await Tm.delete()


@USU.UBOT("ungmute")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    _msg = f"<i><b>{prs}Processing...</b></i>"

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        try:
            await client.unban_chat_member(dialog, user.id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.unban_chat_member(dialog, user.id)
                done += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1
    text = f"""<i><b>{broad}Global Unmuted!
{sks}Success: {done} chats
{ggl}Failed: {failed} chats
{ptr}User: <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a></b></i>"""
    await message.reply(text)
    return await Tm.delete()


@USU.UBOT("gban")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    _msg = f"<i><b>{prs}Processing...</b></i>"

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        if user.id == client.me.id:
            return await Tm.edit(f"<i><b>{ggl}Anda tidak bisa gban diri sendiri!</b><i>")
        if user.id in DEVS:
            return await Tm.edit(f"<i><b>{ggl}Anda tidak bisa gban dia karena dia pemilik bot ini!</b><i>")
        try:
            await client.ban_chat_member(dialog, user.id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.ban_chat_member(dialog, user.id)
                done += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1
    text = f"""<i><b>{broad}Global Banned!
{sks}Success: {done} chats
{ggl}Failed: {failed} chats
{ptr}User: <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a></b></i>"""
    await message.reply(text)
    return await Tm.delete()


@USU.UBOT("ungban")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    _msg = f"<i><b>{prs}Processing...</b></i>"

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        try:
            await client.unban_chat_member(dialog, user.id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.unban_chat_member(dialog, user.id)
                done += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1
    text = f"""<i><b>{broad}Global Unbanned!
{sks}Success: {done} chats
{ggl}Failed: {failed} chats
{ptr}User: <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a></b></i>"""
    await message.reply(text)
    return await Tm.delete()


@USU.UBOT("gkick")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    _msg = f"<i><b>{prs}Processing...</b></i>"

    Tm = await message.reply(_msg)
    if not user_id:
        return await Tm.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    done = 0
    failed = 0
    global_id = await get_data_id(client, "global")
    for dialog in global_id:
        if user.id == client.me.id:
            return await Tm.edit(f"<i><b>{ggl}Anda tidak bisa gkick diri sendiri!</b><i>")
        if user.id in DEVS:
            return await Tm.edit(f"<i><b>{ggl}Anda tidak bisa gkick dia karena dia pemilik bot ini!</b><i>")
        try:
            await client.ban_chat_member(dialog, user.id)
            await client.unban_chat_member(dialog, user.id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.ban_chat_member(dialog, user.id)
                await client.unban_chat_member(dialog, user.id)
                done += 1
            except Exception:
                failed += 1
        except Exception:
            failed += 1
    text = f"""<i><b>{broad}Global Kicked!
{sks}Success: {done} chats
{ggl}Failed: {failed} chats
{ptr}User: <a href='tg://user?id={user.id}'>{user.first_name} {user.last_name or ''}</a></b></i>"""
    await message.reply(text)
    return await Tm.delete()

