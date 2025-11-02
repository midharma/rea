import asyncio
import random

from gc import get_objects
from asyncio import sleep

from pyrogram.errors.exceptions import FloodWait
from pyrogram import enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from usu import *




@USU.NO_CMD("PROTECT", ubot)
async def _(client, message):
    if message.reply_to_message:
        return
    wl = await db.get_list_from_vars(client.me.id, "wl")
    if message.from_user and (message.from_user.id in wl or message.from_user.id in DEVS):
        return
    try:
        if message.from_user.id not in await list_admins(client, message.chat.id):
            if message.text:
                word_split = message.text.lower().split()
                word_list = await db.get_vars(client.me.id, "WORD_LIST") or []
                if message.from_user and not message.from_user.is_self or not getattr(message, "outgoing", False):
                    try:
                        await message.delete()
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await message.delete()
                        except Exception:
                            pass
                    except Exception:
                        pass
                if word_list and any(x in word_list for x in word_split):
                    try:
                        await message.delete()
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await message.delete()
                        except Exception:
                            pass
                    except Exception:
                        pass
    except pyrogram.errors.exceptions.forbidden_403.ChatAdminRequired:
        pass
    except Exception as e:
        pass


@USU.NO_CMD("PROTECT_BOT", bot)
async def _(client, message):
    if message.reply_to_message:
        return
    wl = await db.get_list_from_vars(message.chat.id, "wl")
    if message.from_user and (message.from_user.id in wl or message.from_user.id in DEVS):
        return
    try:
        if message.from_user.id not in await list_admins(client, message.chat.id):
            if message.text:
                word_split = message.text.lower().split()
                word_list = await db.get_vars(client.me.id, "WORD_LIST") or []
                mention = f"<b><i><blockquote>{message.from_user.mention} Teks anda terdeteksi Broadcast!</blockquote></i></b>"
                if message.from_user and not message.from_user.is_self or not getattr(message, "outgoing", False):
                    try:
                        await message.delete()
                        anjay = await bot.send_message(message.chat.id, mention)
                        await asyncio.sleep(3)
                        await anjay.delete()
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await message.delete()
                            anjay = await bot.send_message(message.chat.id, mention)
                            await asyncio.sleep(3)
                            await anjay.delete()
                        except Exception:
                            pass
                    except Exception:
                        pass
                if word_list and any(x in word_list for x in word_split):
                    try:
                        await message.delete()
                        anjay = await bot.send_message(message.chat.id, mention)
                        await asyncio.sleep(3)
                        await anjay.delete()
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await message.delete()
                            anjay = await bot.send_message(message.chat.id, mention)
                            await asyncio.sleep(3)
                            await anjay.delete()
                        except Exception:
                            pass
                    except Exception:
                        pass
    except pyrogram.errors.exceptions.forbidden_403.ChatAdminRequired:
        pass
    except Exception as e:
        pass



@USU.CALLBACK("^ankes")
async def _(c, cq):
    button = BTN.TAMBAH()
    pesan = f"""<i><b>Halo,
Saya adalah menu [AntiGcast]({PHOTO})

Command Admins:</b>
/ankes - on/off
/bl - reply/text
/unbl - reply/text
/addwl - reply/username
/delwl - reply/username
/listwl - menampilkan daftar wl
/listbl - menampilkan daftar bl</i>

<b>Catatan:</b>
<i>Jika fitur /ankes on, maka otomatis akan menonaktifkan fitur /chatbot</i>"""
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))
    

@USU.UBOT("ankes")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(client.me.id, "ON_OFF_WORD")
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>`"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    if command == "on":
        if not vars:
            await db.set_vars(client.me.id, "ON_OFF_WORD", query[command])
            return await message.reply(f"<i><b>{sks}Antigcast on!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Antigcast sudah on sebelumnya!</b></i>")
    else:
        if vars:
            await db.set_vars(client.me.id, "ON_OFF_WORD", query[command])
            return await message.reply(f"<i><b>{sks}Antigcast off!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Antigcast sudah off sebelumnya!</b></i>")


@USU.UBOT("addword")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(client.me.id, "WORD_LIST") or []
    text = get_arg(message).split()
   
    add_word = [x for x in text if x not in vars]
    vars.extend(add_word)
    await db.set_vars(client.me.id, "WORD_LIST", vars)
   
    if add_word:
        response = f"<i><b>{sks}Added to antigcast!</b></i>"
    else:
        response = f"<i><b>{ggl}Already in antigcast!</b></i>"

    usu = await message.reply(response)
    await asyncio.sleep(5)
    await message.delete()
    await usu.delete()


@USU.UBOT("listword")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(client.me.id, "WORD_LIST") or []
    if vars:
        msg = f"<b>{broad}Daftar word!</b>\n\n"
        for x in vars:
            msg += f" • {x}\n"
        msg += f"<b>\n{sks}Total Word: {len(vars)}</b>"
    else:
        msg = f"<b>Empty!</b>"
        
    return await message.reply(f"<i>{msg}</i>", quote=True)


@USU.UBOT("delword")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(client.me.id, "WORD_LIST") or []
    _, *text = message.command
    removed_list = [x for x in text if x in vars]
    vars = [x for x in vars if x not in removed_list]
    await db.set_vars(client.me.id, "WORD_LIST", vars)

    if removed_list:
        response = f"<i><b>{sks}Removed from antigcast!</b></i>"
    else:
        response = f"<i><b>{ggl}Not in antigcast!</b></i>"
    usu = await message.reply(response)
    await asyncio.sleep(5)
    await message.delete()
    await usu.delete()

@USU.UBOT("addwl")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    wl = await db.get_list_from_vars(client.me.id, "wl")
    if not user_id:
        return await msg.edit(
            f"<i><b>{ggl}{message.text} user_id/reply</b></i>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    if user.id in wl:
        return await msg.edit(f"<i><b>{ggl}Already in whitelist!</b></i>")
    else:
        await db.add_to_vars(client.me.id, "wl", user.id)
        return await msg.edit(f"<i><b>{sks}Successfully added to whitelist!</b></i>")


@USU.UBOT("delwl")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    wl = await db.get_list_from_vars(client.me.id, "wl")
    if not user_id:
        return await msg.edit(
            f"<i><b>{ggl}{message.text} user_id/reply</b></i>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    if user.id not in wl:
        return await msg.edit(f"<i><b>{ggl}Not in whitelist!</b></i>")
    else:
        await db.remove_from_vars(client.me.id, "wl", user.id)
        return await msg.edit(f"<i><b>{sks}Successfully removed from whitelist!</b></i>")


@USU.UBOT("listwl")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Sh = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    wl = await db.get_list_from_vars(client.me.id, "wl")

    if not wl:
        return await Sh.edit(f"<i><b>{ggl}Empty!</b></i>")

    wl_list = []
    for user_id in wl:
        try:
            user = await client.get_users(int(user_id))
            wl_list.append(
                f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except:
            continue

    if wl_list:
        response = (
            f"<i><b>{broad}Daftar whitelist:</b>\n\n"
            + "\n".join(wl_list)
            + f"\n\n<b>{sks}Total whitelist:</b> <code>{len(wl_list)}</code></i>"
        )
        return await Sh.edit(response)

@USU.BOT("ankes")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(message.chat.id, "ON_OFF_WORD")
    group = await db.get_list_from_vars(bot.me.id, "group")
    if message.chat.id not in group:
        if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
            await db.add_to_vars(bot.me.id, "group", message.chat.id)
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>`"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    if command == "on":
        if not vars:
            await db.set_vars(message.chat.id, "ON_OFF_WORD", query[command])
            await db.set_vars(message.chat.id, "AI_ON_OFF", False)
            return await message.reply(f"<i><b>{sks}Antigcast on!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Antigcast sudah on sebelumnya!</b></i>")
    else:
        if vars:
            await db.set_vars(message.chat.id, "ON_OFF_WORD", query[command])
            return await message.reply(f"<i><b>{sks}Antigcast off!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Antigcast sudah off sebelumnya!</b></i>")


@USU.BOT("bl")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(message.chat.id, "WORD_LIST") or []
    text = get_arg(message).split()
   
    add_word = [x for x in text if x not in vars]
    vars.extend(add_word)
    await db.set_vars(message.chat.id, "WORD_LIST", vars)
   
    if add_word:
        response = f"<i><b>{sks}Added to antigcast!</b></i>"
    else:
        response = f"<i><b>{ggl}Already in antigcast!</b></i>"

    usu = await message.reply(response)
    await asyncio.sleep(5)
    await message.delete()
    await usu.delete()


@USU.BOT("listbl")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(message.chat.id, "WORD_LIST") or []
    if vars:
        msg = f"<b>{broad}Daftar word!</b>\n\n"
        for x in vars:
            msg += f" • {x}\n"
        msg += f"<b>\n{sks}Total Word: {len(vars)}</b>"
    else:
        msg = f"<b>Empty!</b>"
        
    return await message.reply(f"<i>{msg}</i>", quote=True)


@USU.BOT("unbl")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(message.chat.id, "WORD_LIST") or []
    _, *text = message.command
    removed_list = [x for x in text if x in vars]
    vars = [x for x in vars if x not in removed_list]
    await db.set_vars(message.chat.id, "WORD_LIST", vars)

    if removed_list:
        response = f"<i><b>{sks}Removed from antigcast!</b></i>"
    else:
        response = f"<i><b>{ggl}Not in antigcast!</b></i>"
    usu = await message.reply(response)
    await asyncio.sleep(5)
    await message.delete()
    await usu.delete()

@USU.BOT("addwl")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    wl = await db.get_list_from_vars(message.chat.id, "wl")
    if not user_id:
        return await msg.edit(
            f"<i><b>{ggl}{message.text} user_id/reply</b></i>"
        )
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    if user.id in wl:
        return await msg.edit(f"<i><b>{ggl}Already in whitelist!</b></i>")
    else:
        await db.add_to_vars(message.chat.id, "wl", user.id)
        return await msg.edit(f"<i><b>{sks}Successfully added to whitelist!</b></i>")


@USU.BOT("delwl")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    wl = await db.get_list_from_vars(message.chat.id, "wl")
    if not user_id:
        return await msg.edit(
            f"<i><b>{ggl}{message.text} user_id/reply</b></i>"
        )
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    if user.id not in wl:
        return await msg.edit(f"<i><b>{ggl}Not in whitelist!</b></i>")
    else:
        await db.remove_from_vars(message.chat.id, "wl", user.id)
        return await msg.edit(f"<i><b>{sks}Successfully removed from whitelist!</b></i>")


@USU.BOT("listwl")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Sh = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    wl = await db.get_list_from_vars(message.chat.id, "wl")
    await message.delete()
    if not wl:
        return await Sh.edit(f"<i><b>{ggl}Empty!</b></i>")
    wl_list = []
    for user_id in wl:
        try:
            user = await client.get_users(int(user_id))
            wl_list.append(
                f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except:
            continue

    if wl_list:
        response = (
            f"<i><b>{broad}Daftar whitelist:</b>\n\n"
            + "\n".join(wl_list)
            + f"\n\n<b>{sks}Total whitelist:</b> <code>{len(wl_list)}</code></i>"
        )
        return await Sh.edit(response)