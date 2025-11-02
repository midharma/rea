import os
import asyncio
import random

from os import remove
from asyncio import sleep, gather

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.enums import ChatType

from usu import *




@USU.UBOT("sg")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    get_user = await extract_user(message)
    lol = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not get_user:
        return await lol.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user_id = (await client.get_users(get_user)).id
    except Exception:
        try:
            user_id = int(message.command[1])
        except Exception as error:
            return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    getbot = random.choice(bot)
    await client.unblock_user(getbot)
    txt = await client.send_message(getbot, user_id)
    await asyncio.sleep(4)
    await txt.delete()
    await lol.delete()
    async for name in client.search_messages(getbot, limit=2):
        if not name.text:
            await message.reply(
                f"<i><b>{ggl}Maaf {getbot} invalid!</b></i>")
        else:
            await message.reply(name.text, quote=True)
    user_info = await client.resolve_peer(getbot)
    return await client.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))



@USU.UBOT("info")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not user_id:
        return await Tm.edit(
            f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b>Information!</b>
 
<b>User ID:</b> <code>{user.id}</code> 
<b>First Name:</b> {first_name} 
<b>Last Name:</b> {last_name} 
<b>Username:</b> {username} 
<b>Dc ID:</b> <code>{dc_id}</code> 
<b>Is Bot:</b> <code>{user.is_bot}</code> 
<b>Is Scam:</b> <code>{user.is_scam}</code> 
<b>Restricted:</b> <code>{user.is_restricted}</code> 
<b>Verified:</b> <code>{user.is_verified}</code> 
<b>Premium:</b> <code>{user.is_premium}</code> 
<b>Bio:</b> {bio} 
<b>Same Group:</b> {len(common)} 
<b>Last Seen:</b> <code>{status}</code> 
<b>Mention:</b> <a href=tg://user?id={user.id}>{fullname}</a> 
"""

        await Tm.edit(f"<i>{out_str}</i>", disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(e)


@USU.UBOT("gcinfo")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Tm = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    try:
        if len(message.text.split()) > 1:
            chat_u = message.text.split()[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await Tm.edit(
                    f"<i><b>{ggl}Invalid!</b></i>"
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Private"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b>Information!</b> 

<b>Chat ID:</b> <code>{chat.id}</code> 
<b>Title:</b> {chat.title} 
<b>Username:</b> {username} 
<b>Type:</b> <code>{type}</code> 
<b>Dc ID:</b> <code>{dc_id}</code> 
<b>Is Scam:</b> <code>{chat.is_scam}</code> 
<b>Is Fake:</b> <code>{chat.is_fake}</code> 
<b>Verified:</b> <code>{chat.is_verified}</code> 
<b>Restricted:</b> <code>{chat.is_restricted}</code> 
<b>Protected:</b> <code>{chat.has_protected_content}</code> 
<b>Total Member:</b> <code>{chat.members_count}</code> 
<b>Description:</b> <code>{description}</code> 
"""

        await Tm.edit(f"<i>{out_str}</i>", disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(e)




@USU.UBOT("id")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    text = f"<b>Message ID:</b> {message.id}\n"

    if message.chat.type == ChatType.CHANNEL:
        text += f"<b>Chat ID:</b> {message.sender_chat.id}\n"
    else:
        text += f"<b>Your ID:</b> {message.from_user.id}\n\n"

        if len(message.command) > 1:
            try:
                user = await client.get_chat(message.text.split()[1])
                text += f"<b>User ID:</b> {user.id}\n\n"
            except:
                return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")

        text += f"<b>Chat ID:</b> {message.chat.id}\n\n"

    if message.reply_to_message:
        id_ = (
            message.reply_to_message.from_user.id
            if message.reply_to_message.from_user
            else message.reply_to_message.sender_chat.id
        )
        file_info = get_file_id(message.reply_to_message)
        if file_info:
            text += f"<b>Media ID:</b> {file_info.file_id}\n\n"
        text += (
            f"<b>Replied Message ID:</b> {message.reply_to_message.id}\n"
            f"<b>Replied User ID:</b> {id_}"
        )

    return await message.reply(f"<i>{text}</i>", disable_web_page_preview=True)

@USU.UBOT("idm")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    usu = message.reply_to_message
    if not usu:
        return await message.reply_text(f"<i><b>{prs}Processing...</b></i>")
    try:
        emoji_text = usu.text
        emoji_id = usu.entities[0].custom_emoji_id
        await message.reply_text(f"`<emoji id={emoji_id}>{emoji_text}</emoji>`", parse_mode=ParseMode.MARKDOWN)
    except NoneType:
        await message.reply_text(f"<i><b>{ggl}Error!</b></i>")

@USU.UBOT("setbio")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    tex = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) == 1:
        return await tex.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[text]</b></i>")
    elif message.reply_to_message and message.reply_to_message.text:
        bio = message.reply_to_message.text
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
    try:
        await client.update_profile(bio=bio)
        await tex.edit(f"<i><b>{sks}Success changing bio!</b></i>")
    except Exception as e:
        await tex.edit(f"<i><b>{ggl}Error:</b> <code>{e}</code></i>")


@USU.UBOT("setname")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    tex = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) == 1:
        return await tex.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[text]</b></i>")
    elif message.reply_to_message and message.reply_to_message.text:
        name = message.reply_to_message.text
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
    try:
        await client.update_profile(first_name=name)
        await tex.edit(f"<i><b>{sks}Success changing name!</b></i>")
    except Exception as e:
        await tex.edit(f"<i><b>{ggl}Error:</b> <code>{e}</code></i>")


@USU.UBOT("block")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    tex = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not user_id:
        return await tex.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[reply]</b></i>")
    if user_id == client.me.id:
        return await tex.edit(f"<i><b>{ggl}Invalid!</b></i>")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"<i><b>{sks}Successfully blocked!</b></i>")
  

@USU.UBOT("unblock")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    tex = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not user_id:
        return await tex.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[reply]</b></i>")
    if user_id == client.me.id:
        return await tex.edit(f"<i><b>{ggl}Invalid!</b></i>")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit(f"<i><b>{sks}Successfully unblocked!</b></i>")


@USU.UBOT("setpp")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    rep = message.reply_to_message
    tex = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not rep or (not rep.photo and not rep.video):
        return await tex.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[reply]</b></i>")
    try:
        file = await rep.download()
        if rep.photo:
            await client.set_profile_photo(photo=file)
        elif rep.video:
            await client.set_profile_photo(video=file)
        os.remove(file)
        return await tex.edit(f"<i><b>{sks}Successfully set profile!</b></i>")
    except Exception as e:
        return await tex.edit(f"<i><b>{ggl}Error!</b></i>")



#============

@USU.BOT("setname")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    tex = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) == 1:
        return await tex.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[text]</b></i>")
    elif message.reply_to_message and message.reply_to_message.text:
        name = message.reply_to_message.text
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
    try:
        await client.usu.update_profile(first_name=name)
        await tex.edit(f"<i><b>{sks}Success changing name!</b></i>")
    except Exception as e:
        await tex.edit(f"<i><b>{ggl}Error:</b> <code>{e}</code></i>")


@USU.BOT("setbio")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    tex = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) == 1:
        return await tex.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[text]</b></i>")
    elif message.reply_to_message and message.reply_to_message.text:
        bio = message.reply_to_message.text
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
    try:
        await client.usu.update_profile(bio=bio)
        await tex.edit(f"<i><b>{sks}Success changing bio!</b></i>")
    except Exception as e:
        await tex.edit(f"<i><b>{ggl}Error:</b> <code>{e}</code></i>")



@USU.BOT("id")
@USU.ADMIN
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    text = f"<b>Message ID:</b> {message.id}\n"

    if message.chat.type == ChatType.CHANNEL:
        text += f"<b>Chat ID:</b> {message.sender_chat.id}\n"
    else:
        text += f"<b>Your ID:</b> {message.from_user.id}\n\n"

        if len(message.command) > 1:
            try:
                user = await client.get_chat(message.text.split()[1])
                text += f"<b>User ID:</b> {user.id}\n\n"
            except:
                return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")

        text += f"<b>Chat ID:</b> {message.chat.id}\n\n"

    if message.reply_to_message:
        id_ = (
            message.reply_to_message.from_user.id
            if message.reply_to_message.from_user
            else message.reply_to_message.sender_chat.id
        )
        file_info = get_file_id(message.reply_to_message)
        if file_info:
            text += f"<b>Media ID:</b> {file_info.file_id}\n\n"
        text += (
            f"<b>Replied Message ID:</b> {message.reply_to_message.id}\n"
            f"<b>Replied User ID:</b> {id_}"
        )

    return await message.reply(f"<i>{text}</i>", disable_web_page_preview=True)

@USU.BOT("sg")
@USU.ADMIN
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    get_user = await extract_user(message)
    lol = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not get_user:
        return await lol.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user_id = (await client.usu.get_users(get_user)).id
    except Exception as error:
        return await lol.edit(error)
    bot = ["@Sangmata_bot", "@SangMata_beta_bot"]
    getbot = random.choice(bot)
    await client.usu.unblock_user(getbot)
    txt = await client.usu.send_message(getbot, user_id)
    await asyncio.sleep(4)
    await txt.delete()
    await lol.delete()
    async for name in client.usu.search_messages(getbot, limit=2):
        if not name.text:
            await message.reply(
                f"<i><b>{ggl}Maaf {getbot} invalid!</b></i>")
        else:
            await message.reply(name.text, quote=True)
    user_info = await client.usu.resolve_peer(getbot)
    return await client.usu.invoke(DeleteHistory(peer=user_info, max_id=0, revoke=True))



@USU.BOT("info")
@USU.ADMIN
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    Tm = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if not user_id:
        return await Tm.edit(
            f"<i><b>{ggl}Invalid!</b></i>")
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        out_str = f"""<b>Information!</b>
 
<b>User ID:</b> <code>{user.id}</code> 
<b>First Name:</b> {first_name} 
<b>Last Name:</b> {last_name} 
<b>Username:</b> {username} 
<b>Dc ID:</b> <code>{dc_id}</code> 
<b>Is Bot:</b> <code>{user.is_bot}</code> 
<b>Is Scam:</b> <code>{user.is_scam}</code> 
<b>Restricted:</b> <code>{user.is_restricted}</code> 
<b>Verified:</b> <code>{user.is_verified}</code> 
<b>Premium:</b> <code>{user.is_premium}</code> 
<b>Bio:</b> {bio} 
<b>Last Seen:</b> <code>{status}</code> 
<b>Mention:</b> <a href=tg://user?id={user.id}>{fullname}</a> 
"""

        await Tm.edit(f"<i>{out_str}</i>", disable_web_page_preview=True)
    except Exception as e:
        return await Tm.edit(e)

