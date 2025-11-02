
import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    ChatNotModified,
)

import random
import re

from pyrogram import filters, Client
from asyncio import sleep
from re import search, IGNORECASE, escape

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from re import findall

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

from usu import *

@USU.CALLBACK("^manage")
async def _(c, cq):
    button = BTN.TAMBAH()
    pesan = f"""<i><b>Halo,
Saya adalah menu [Manage]({PHOTO})

Format Set (Welcome/GoodBye):</b>
&#123;mention&#125; - menyebut pengguna
&#123;user_id&#125; - menampilkan id pengguna
&#123;first_name&#125; - menampilkan nama depan pengguna
&#123;last_name&#125; - menampilkan nama belakang pengguna
&#123;username&#125; - menampilkan username pengguna
&#123;chat_title&#125; - menampilkan nama group
&#123;chat_id&#125; - menampilkan id group

<b>Contoh Format Button/None:</b>
• Halo &#123;mention&#125;, Selamat datang di group &#123;chat_title&#125;
• Halo &#123;mention&#125;, Selamat datang di group &#123;chat_title&#125; | NamaButton1 - link1 | NamaButton2 - link2 |

<b>Format Font:</b>
&lt;b&gt;: Bold/Tebal - Teks tebal
&lt;i&gt;: Italic/Miring - Teks miring
&lt;u&gt;: Underline/GarisBawah - Teks garis bawah
&lt;s&gt;: Strikethrought/GarisTengah - Teks coret
&lt;code&gt;: Code/Monospace - Teks bisa di salin

<b>Contoh Format Font:</b>
• &lt;b&gt;Halo &#123;mention&#125;, Selamat datang di group &#123;chat_title&#125;&lt;/b&gt;

<b>Command Devs:</b>
/gban - blokir pengguna di semua chat bot admin
/ungban - lepas blokir pengguna di semua chat bot admin
/gmute  - bisukan pengguna di semua chat bot admin
/ungmute - melepas bisu pengguna di semua chat bot admin
/gkick - tendang pengguna di semua chat bot admin
/addsudo - menambahkan akses devs ke pengguna sudo bot
/delsudo - menghapus akses devs di pengguna sudo bot
/clearsudo - menghapus akses devs di semua pengguna sudo bot
/listsudo - melihat daftar pengguna sudo

<b>Command Admins:</b>
/staff - melihat daftar admin
/setwelcome - menampilkan pesan selamat datang
/delwelcome - menghapus pesan selamat datang
/id - cek id
/sg - cek history nama pengguna
/info - cek informasi pengguna
/ban - blokir pengguna dari chat
/unban - lepas blokir pengguna dari chat
/mute - membisukan pengguna dari chat
/unmute - melepas bisu pengguna dari chat
/kick - tendang pengguna dari chat
/listvc - cek pengguna yang ada di obrolan suara
/setvc - mengganti judul obrolan suara
/startvc - memulai obrolan suara
/stopvc - mematikan obrolan suara
/filter - on/off
/addfilter - nama_filter - reply
/delfilter - nama_filter
/clearfilter - menghapus semua nama filter
/filters - melihat daftar nama filter
/del - menghapus pesan yang di reply</i>"""
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))



@USU.NO_CMD("FILTERS_GC_BOT", bot)
async def _(client, message):
    try:
        all_filters = await db.all_vars(message.chat.id, "FILTERS_GC") or {}

        for key, value in all_filters.items():
            if key in message.text.lower().split():
                return await message.reply(value)
    except ChatAdminRequired:
        pass
    except BaseException:
        pass


@USU.BOT("pin")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if not message.reply_to_message:
        return await message.reply(f"<b><i>{ggl}Reply text!</i></b>")
    r = message.reply_to_message
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_pin_messages) and admin.user.id not in DEVS:
        return await message.reply(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        await r.pin()
        return await message.reply(
            f"<b><i>{sks}Pinned!</i></b>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await message.reply(f"<b><i>{ggl}Not access!</i></b>")

@USU.BOT("unpin")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if not message.reply_to_message:
        return await message.reply(f"<b><i>{ggl}Reply text!</i></b>")
    r = message.reply_to_message
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_pin_messages) and admin.user.id not in DEVS:
        return await message.reply(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        await r.unpin()
        return await message.reply(
            f"<b><i>{sks}Unpinned!</i></b>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        return await message.reply(f"<b><i>{ggl}Not access!</i></b>")


@USU.BOT("admin")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    biji = await eor(message, f"<b><i>{prs}Processing...</i></b>")
    replied = message.reply_to_message
    usu = message.command
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_promote_members) and admin.user.id not in DEVS:
        return await biji.edit(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        if replied:
            user_id = replied.from_user.id
            title = " ".join(usu[1:])
        elif len(usu) > 1 and usu[1].isdigit():
            user_id = int(usu[1])
            title = " ".join(usu[2:])
        elif len(usu) > 1:
            if usu[1].isdigit():
                user_id = int(usu[1])
                title = " ".join(usu[2:])
            else:
                try:
                    user_id = (await client.resolve_peer(usu[1])).user_id
                    title = " ".join(usu[2:])
                except Exception as error:
                    return await biji.edit(error)
        else:
            return await biji.edit(f"<i><b>{ggl}reply/user_id - title</b></i>")
        
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        )
        await message.chat.promote_member(user_id, privileges=privileges)
        await client.set_administrator_title(message.chat.id, user_id, title)
        await biji.edit(f"<b><i>{sks}Berhasil memberikan hak admin!</i></b>")
    
    except ChatAdminRequired:
        await biji.edit(f"<b><i>{ggl}Not access!</i></b>")


@USU.BOT("fulladmin")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    biji = await eor(message, f"<b><i>{prs}Processing...</i></b>")
    replied = message.reply_to_message
    usu = message.command
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_promote_members) and admin.user.id not in DEVS:
        return await biji.edit(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        if replied:
            user_id = replied.from_user.id
            title = " ".join(usu[1:])
        elif len(usu) > 1 and usu[1].isdigit():
            user_id = int(usu[1])
            title = " ".join(usu[2:])
        elif len(usu) > 1:
            if usu[1].isdigit():
                user_id = int(usu[1])
                title = " ".join(usu[2:])
            else:
                try:
                    user_id = (await client.resolve_peer(usu[1])).user_id
                    title = " ".join(usu[2:])
                except Exception as error:
                    return await biji.edit(error)
        else:
            return await biji.edit(f"<i><b>{ggl}reply/user_id - title</b></i>")
        
        privileges = ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=True,
        )
        await message.chat.promote_member(user_id, privileges=privileges)
        await client.set_administrator_title(message.chat.id, user_id, title)
        await biji.edit(f"<b><i>{sks}Berhasil memberikan hak admin!</i></b>")
    
    except ChatAdminRequired:
        await biji.edit(f"<b><i>{ggl}Not access!</i></b>")


@USU.BOT("unadmin")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    sempak = await eor(message, f"<b><i>{prs}Processing...</i></b>")
    if not user_id:
        return await sempak.edit(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
    if user_id == client.me.id:
        return await sempak.edit(f"<b><i>{ggl}Reply pengguna lain!</i></b>")
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_promote_members) and admin.user.id not in DEVS:
        return await sempak.edit(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    await asyncio.sleep(1)
    umention = (await client.get_users(user_id)).mention
    await sempak.edit(f"<b><i>{sks}Lepas hak admin!</i></b>")


@USU.BOT("unban")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_restrict_members) and admin.user.id not in DEVS:
        return await message.reply(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    try:
        await message.chat.unban_member(user_id)
        await message.reply(f"<b><i>{sks}Success unban pengguna!</i></b>")
    except Exception as error:
        await message.reply(error)

@USU.BOT("ban")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
    if user_id in DEVS:
        return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.reply_text(
            f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
        )
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_restrict_members) and admin.user.id not in DEVS:
        return await message.reply(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    msg_ban = f"""<b><i>{sks}Success ban pengguna!</i></b>"""
    try:
        await message.chat.ban_member(user_id)
        await message.reply(msg_ban)
    except Exception as error:
        await message.reply(error)



@USU.BOT("unmute")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_restrict_members) and admin.user.id not in DEVS:
        return await message.reply(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    try:
        await message.chat.unban_member(user_id)
        await message.reply(f"<b><i>{sks}Success unmute pengguna!</i></b>")
    except Exception as error:
        await message.reply(error)

@USU.BOT("mute")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
    if user_id in DEVS:
        return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.reply_text(
            f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
        )
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_restrict_members) and admin.user.id not in DEVS:
        return await message.reply(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    msg_mute = f"""<b><i>{sks}Success mute pengguna!</i></b>"""
    try:
        await message.chat.restrict_member(user_id, ChatPermissions())
        await message.reply(msg_mute)
    except Exception as error:
        await message.reply(error)


@USU.BOT("kick")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
    if user_id in DEVS:
        return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
    if user_id in (await list_admins(client, message.chat.id)):
        return await message.reply_text(
            f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
        )
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if (admin.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR] or not admin.privileges.can_restrict_members) and admin.user.id not in DEVS:
        return await message.reply(f"<i><b>{ggl}Anda tidak memiliki hak admin yang cukup!</b></i>")
    try:
        mention = (await client.get_users(user_id)).mention
    except Exception as error:
        await message.reply(error)
    msg_kick = f"""<b><i>{sks}Success kick pengguna!</i></b>"""
    try:
        await message.chat.ban_member(user_id)
        await message.reply(msg_kick)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except Exception as error:
        await message.reply(error)


@USU.BOT("filter")
@USU.GROUP
@USU.ADMIN
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
    await db.set_vars(message.chat.id, "FILTERS_GC_ON_OFF", type)
    return await txt.edit(f"<i><b>{sks}Successfully set to mode: {type}</b></i>")


@USU.BOT("addfilter")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    txt = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    type, reply = extract_type_and_msg(message)
    all = await db.all_vars(message.chat.id, "FILTERS_GC") or {}
    if not type and message.reply_to_message:
        return await txt.edit(f"<i><b>{ggl}Reply text or enter text</b></i>")
    if type not in all:
        try:
            await db.set_vars(message.chat.id, type, str(reply.text), "FILTERS_GC")
            await txt.edit(f"<i><b>{sks}Message:</b> <code>{type}</code> <b>Successfully added to filter</b></i>")
        except Exception as error:
            await txt.edit(error)
    else:
        return await txt.edit(f"<i><b>{ggl}Cannot create new a filter</b></i>")


@USU.BOT("delfilter")
@USU.GROUP
@USU.ADMIN
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
    all = await db.all_vars(message.chat.id, "FILTERS_GC") or {}

    if arg not in all:
        return await txt.edit(f"<i><b>{ggl}Message:</b> <code>{arg}</code> <b>Not found!</b></i>")

    await db.remove_vars(message.chat.id, arg, "FILTERS_GC")
    return await txt.edit(f"<i><b>{sks}Message:</b> <code>{arg}</code> <b>Successfully removed to filter</b></i>")

@USU.BOT("clearfilter")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    txt = await message.reply(f"<i><b>{prs}Processing...</b></i>")

    all = await db.all_vars(message.chat.id, "FILTERS_GC")
    for anu in all:
        await db.remove_vars(message.chat.id, anu, "FILTERS_GC")
    return await txt.edit(f"<i><b>{sks}Successfully removed all filter</b></i>")


@USU.BOT("filters")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    all_filters = await db.all_vars(message.chat.id, "FILTERS_GC")
    if all_filters:
        msg = f"{broad}List filters\n"
        for x in all_filters.keys():
            msg += f"{x}\n"
        msg += f"{sks}Total filters: {len(all_filters)}"
    else:
        msg = f"<b>{ggl}Filters not found!</b>"

    await message.reply(f"<i>{msg}</i>", quote=True)


@USU.BOT("gmute")
@USU.SUDO
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
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    chat = []
    chat.extend(group)
    chat.extend(channel)
    for dialog in chat:
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


@USU.BOT("ungmute")
@USU.SUDO
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
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    chat = []
    chat.extend(group)
    chat.extend(channel)
    for dialog in chat:
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


@USU.BOT("gban")
@USU.SUDO
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
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    chat = []
    chat.extend(group)
    chat.extend(channel)
    for dialog in chat:
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


@USU.BOT("ungban")
@USU.SUDO
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
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    chat = []
    chat.extend(group)
    chat.extend(channel)
    for dialog in chat:
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


@USU.BOT("gkick")
@USU.SUDO
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
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    chat = []
    chat.extend(group)
    chat.extend(channel)
    for dialog in chat:
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


@USU.BOT("del")
@USU.ADMIN
async def _(client, message):
    rep = message.reply_to_message
    await message.delete()
    if rep:
        await rep.delete()