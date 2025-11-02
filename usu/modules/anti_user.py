import asyncio
import random

from pyrogram import *
from pyrogram import types
from asyncio import sleep

from usu import *




@USU.NO_CMD("ANTI_USERS", ubot)
async def _(client, message):
    is_users = await db.get_list_from_vars(client.me.id, "BL_USERS") or []
    user_id = message.from_user.id if message.from_user else message.sender_chat.id
   
    if user_id in is_users:
        try:
            await message.delete()
        except Exception as e:
            await message.reply("<b><i>Error!</i></b>")

    elif message.text is None:
        try:
            await message.delete()
        except Exception as e:
            await message.reply("<b><i>Error!</i></b>")


@USU.UBOT("antiuser")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</i></b>"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    txt = (
        f"<i><b>{sks}Antiuser on!</b></i>"
        if command == "on"
        else f"<i><b>{sks}Antiuser off!</b></i>"
    )
    await db.set_vars(client.me.id, "ON_OFF_DOR", query[command])
    await message.reply(txt)

@USU.UBOT("dor")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<i><b>{ggl}{message.text} user_id/username</b></i>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await db.get_list_from_vars(client.me.id, "BL_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
<b><i>{ggl}Already on the antiuser!</i></b>
"""
        )

    try:
        await db.add_to_vars(client.me.id, "BL_USERS", user.id)
        await msg.edit(f"""
<b><i>{sks}Added to antiuser!</i></b>
"""
        )
        await asyncio.sleep(5)
        await message.delete()
        await msg.delete()
    except Exception as error:
        return await msg.edit(error)


@USU.UBOT("undor")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<b><i>{prs}Processing...</i></b>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><i>{ggl}{message.text} user_id/username</i></b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await db.get_list_from_vars(client.me.id, "BL_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
<b><i>{ggl}Not in antiuser!</i></b>
"""
        )
    try:
        await db.remove_from_vars(client.me.id, "BL_USERS", user.id)
        await msg.edit(f"""
<b><i>{sks}Removed from antiuser!</i></b>
"""
        )
        await asyncio.sleep(5)
        await message.delete()
        await msg.delete()
    except Exception as error:
        return await msg.edit(error)


@USU.UBOT("listdor")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Sh = await message.reply(f"<b><i>{prs}Processing...</i></b>")
    admin_users = await db.get_list_from_vars(client.me.id, "BL_USERS")

    if not admin_users:
        return await Sh.edit(f"<b><i>{ggl}Empty!</i></b>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"<b><i>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></i></b>"
            )
        except:
            continue

    if admin_list:
        response = (
            f"<b><i>{broad}Antiuser list:</i></b>\n\n"
            + "\n".join(admin_list)
            + f"\n\n<i><b>{sks}Total antiuser:</b> <code>{len(admin_list)}</code></i>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("<b><i>{ggl}Error!</i></b>")
