import asyncio

from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    ChatNotModified,
)

from pyrogram.errors import BotResponseTimeout, QueryIdInvalid
from gc import get_objects
from usu import *
 
LOCKS = """Command for <b>Permissions</b>

<b>Permissions</b>
 <i>melihat daftar izin group</i>
    <code>{0}perm</code>"""

CHATBOT = """Command for <b>ChatBot-AI</b>

<b>ChatBot-AI</b>
 <i>mengaktifkan/nonaktifkan chatbot</i>
    <code>{0}chatbot</code> [on/off]
 <i>melihat daftar group yang aktifkan chatbot</i>
    <code>{0}listchatbot</code>
 <i>menghapus semua group yang aktifkan chatbot</i>
    <code>{0}clearchatbot</code>

<b>Catatan:</b>
 <i>Fitur ini bekerja kalau anda admin di group tersebut</i>"""

MUTES = """Command for <b>Mutes</b>

<b>Mutes</b>
 <i>bisukan anggota group</i>
    <code>{0}mute</code>
 <i>melepas pembisuan anggota group</i>
    <code>{0}unmute</code>"""

BANS = """
Command for <b>Bans</b>

<b>Bans</b>
 <i>memblokir anggota group</i>
    <code>{0}ban</code>
 <i>membuka blokir anggota group</i>
    <code>{0}unban</code>"""

ZOMBIES = """Command for <b>Zombies</b>

<b>Zombies</b>
 <i>mengeluarkan akun terhapus</i>
    <code>{0}zombies</code>"""

KICKS = """Command for <b>Kicks</b>

<b>Kicks</b>
 <i>mendang anggota group</i>
    <code>{0}kick</code>"""

PINS = """Command for <b>Pins</b>

<b>Pins</b>
 <i>sematkan pesan</i>
    <code>{0}pin</code>
 <i>lepas sematan pesan</i>
    <code>{0}unpin</code>"""

PROMOTE = """Command for <b>Promote</b>
 
<b>Promote</b>
 <i>adminkan anggota group</i>
    <code>{0}admin or {0}fulladmin</code>
 <i>turunkan admin anggota group</i>
    <code>{0}unadmin</code>"""

ANTIUSER = """Command for <b>Anti-User</b>

<b>Blacklist user</b>
 <i>mengaktifkan/nonaktifkan antiuser</i>
    <code>{0}antiuser [on/off]</code>
 <i>tambahkan pengguna dalam blacklist</i>
    <code>{0}dor</code>
 <i>hapus pengguna dalam blacklist</i>
    <code>{0}undor</code>
 <i>melihat daftar blacklist</i>
    <code>{0}listdor</code>

<b>Notes:</b>
<i>pengguna yang di tambahkan tidak bisa 
mengirim pesan digroup yang anda admin</i>"""

ANTIGCAST = """Command for <b>Antigcast</b>

<b>Antigcast</b>
 <i>mengaktifkan/nonaktifkan antigcast</i>
    <code>{0}ankes [on/off]</code>
 <i>tambahkan pengguna whitelist dalam antigcast</i>
    <code>{0}addwl [user_id/reply]</code>
 <i>hapus pengguna whitelist dalam antigcast</i>
    <code>{0}delwl [user_id/reply]</code>
 <i>tambahkan kata-kata dalam antigcast</i>
    <code>{0}addword [text/reply]</code>
 <i>hapus kata-kata dalam antigcast</i>
    <code>{0}delword [text/reply]</code>
 <i>melihat daftar kata-kata antigcast</i>
    <code>{0}listword</code>

<b>Catatan:</b>
<i>jika antigcast on maka sistem otomatis detect pesan yang bukan tulisan tangan, maka otomatis pesan dihapus!

kata-kata yang di tambahkan tidak bisa 
mengirim pesan digroup yang anda admin</i>"""

DEL = """Command for <b>Del</b>

<b>Delete</b>
 <i>menghapus pesan yang di reply</i>
    <code>{0}del</code> [reply text]"""


__UTAMA__ = "Admins"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Mutes", "Kicks", "Bans", "Pins", "Promote", "Antiuser", "Antigcast", "Del", "Zombies", "ChatBot-AI", "Permissions"
__HASIL__ = MUTES, KICKS, BANS, PINS, PROMOTE, ANTIUSER, ANTIGCAST, DEL, ZOMBIES, CHATBOT, LOCKS


# Daftar permission
data = {
    "msg": "can_send_messages",               # Ngirim pesan
    "media": "can_send_media_messages",       # Foto / video / musik / file
    "url": "can_add_web_page_previews",       # Tautan tertanam
    "polls": "can_send_polls",                # Poll
    "info": "can_change_info",                # Ubah info obrolan
    "invite": "can_invite_users",             # Tambah anggota
    "pin": "can_pin_messages",                # Semat pesan
    "other": "can_send_other_messages",
}

# Ambil permission saat ini
async def current_chat_permissions(client, chat_id):
    perms = []
    try:
        perm = (await client.get_chat(chat_id)).permissions
        if perm.can_send_messages:
            perms.append("can_send_messages")
        if perm.can_send_media_messages:
            perms.append("can_send_media_messages")
        if perm.can_send_other_messages:
            perms.append("can_send_other_messages")
        if perm.can_add_web_page_previews:
            perms.append("can_add_web_page_previews")
        if perm.can_send_polls:
            perms.append("can_send_polls")
        if perm.can_change_info:
            perms.append("can_change_info")
        if perm.can_invite_users:
            perms.append("can_invite_users")
        if perm.can_pin_messages:
            perms.append("can_pin_messages")
    except:
        pass
    return perms

# Buat keyboard
def create_locks_keyboard(permissions, chat_id, msg_id):
    buttons = []
    row = []
    for perm_key, perm_value in data.items():
        button = InlineKeyboardButton(
            perm_key.capitalize(),
            callback_data=f"toggleperm_{chat_id}_{perm_key}_{msg_id}"
        )
        row.append(button)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    # Lock All / Unlock All
    buttons.append([
        InlineKeyboardButton("🔐 Lock All", callback_data=f"kunciall_{chat_id}_{msg_id}"),
        InlineKeyboardButton("🔓 Unlock All", callback_data=f"bukaall_{chat_id}_{msg_id}")
    ])
    return InlineKeyboardMarkup(buttons)

# Update teks inline
async def update_locks_message(user, chat_id, cq, msg_id):
    chat = await user.get_chat(chat_id)
    current_perms = await current_chat_permissions(user, chat_id)
    locked_count = len(data) - len([p for p in data.values() if p in current_perms])
    unlocked_count = len([p for p in data.values() if p in current_perms])
    status_lines = []
    current_perms = await current_chat_permissions(user, chat_id)
    for key, value in data.items():
        icon = "🔓" if value in current_perms else "🔐"
        status_lines.append(f"{icon} {key.capitalize()}")

    status_text = (
        f"<b><i>🔐 Permission Group</i></b>\n\n"
        f"<b>Group:</b> {chat.title}\n\n"
        + "\n".join(status_lines) +
        "\n\n<i>Klik tombol untuk toggle lock/unlock</i>"
    )
    keyboard = create_locks_keyboard(current_perms, chat_id, msg_id)
    try:
        await cq.edit_message_text(status_text, reply_markup=keyboard)
    except Exception as e:
        logger.exception(e)

@USU.UBOT("perm")
@USU.GROUP
async def locks_handler(client, message):
    sks = await EMO.SUKSES(client)
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    try:
        # pesan sementara menandakan loading
        anu = await message.reply(f"{prs}<b>Memuat permission manager...</b>")

        bot_username = bot.me.username  # username userbot
        chat_id = message.chat.id

        # memanggil inline query ke userbot sendiri
        results = await client.get_inline_bot_results(
            bot_username,
            f"lockspanel|{client.me.id}|{chat_id}"
        )

        await client.send_inline_bot_result(
            chat_id=chat_id,
            query_id=results.query_id,
            result_id=results.results[0].id,
            reply_to_message_id=message.id
        )

        await anu.delete()
    except Exception as e:
        await message.reply(f"{ggl}<b>Error: {str(e)}</b>")


@USU.INLINE("lockspanel")
async def inline_locks_handler(client, inline_query):
    query = inline_query.query.lower().strip()
    if not query.startswith("lockspanel"):
        return
    try:
        parts = query.split("|")
        client_id = int(parts[1])
        chat_id = int(parts[2])
        user = ubot._ubot[client_id]
        chat = await user.get_chat(chat_id)
        permissions = await current_chat_permissions(user, chat_id)
        locked_count = len(data) - len([p for p in data.values() if p in permissions])
        unlocked_count = len([p for p in data.values() if p in permissions])
        keyboard = create_locks_keyboard(permissions, chat_id, client_id)
        status_lines = []
        current_perms = await current_chat_permissions(user, chat_id)
        for key, value in data.items():
            icon = "🔓" if value in current_perms else "🔐"
            status_lines.append(f"{icon} {key}")

        status_text = (
            f"<b><i>🔐 Permission Group</i></b>\n\n"
            f"<b>Group:</b> {chat.title}\n\n"
            + "\n".join(status_lines) +
            "\n\n<i>Klik tombol untuk toggle lock/unlock</i>"
        )
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id="lockspanel",
                    title="🔐 Permission Manager",
                    description=f"🔒 {locked_count} Locked | 🔓 {unlocked_count} Unlocked",
                    input_message_content=InputTextMessageContent(status_text),
                    reply_markup=keyboard
                )
            ],
            cache_time=1
        )
    except Exception as e:
        await inline_query.answer(
            results=[
                InlineQueryResultArticle(
                    id="error",
                    title="❌ Error",
                    description=str(e),
                    input_message_content=InputTextMessageContent(f"<b><i>❌ Error: {str(e)}</i></b>")
                )
            ],
            cache_time=1
        )

# Toggle permission
@USU.CALLBACK("toggleperm_")
async def toggle_perm_callback(client, callback_query):
    parts = callback_query.data.split("_")
    if len(parts) < 4:
        return await callback_query.answer("❌ Invalid callback data!", show_alert=True)
    chat_id = int(parts[1])
    perm_key = parts[2]
    client_id = int(parts[3])
    user = ubot._ubot[client_id]
    admin = await list_admins(user, chat_id)
    if callback_query.from_user.id not in admin:
        return await callback_query.answer("❌ Anda bukan admin group ini!", show_alert=True)
    try:
        perm_value = data.get(perm_key)
        current_perms = await current_chat_permissions(user, chat_id)
        keyboard = create_locks_keyboard(current_perms, chat_id, client_id)
        perms_dict = {v: (v in current_perms) for v in data.values()}
        perms_dict[perm_value] = not perms_dict[perm_value]
        await user.set_chat_permissions(chat_id, ChatPermissions(**perms_dict))
        await update_locks_message(user, chat_id, callback_query, client_id)
        await callback_query.answer(
            f"✅ Permission {perm_key} {'dibuka' if perms_dict[perm_value] else 'dikunci'}!",
            show_alert=True
        )
    except ChatAdminRequired:
        await callback_query.answer("❌ Anda tidak punya akses admin!", show_alert=True)
    except Exception as e:
        logger.exception(e)
        await callback_query.answer(f"❌ Error: {str(e)}", show_alert=True)

# Lock All
@USU.CALLBACK("kunciall_")
async def lockall_callback(client, callback_query):
    parts = callback_query.data.split("_")
    if len(parts) < 3:
        return await callback_query.answer("❌ Invalid callback data!", show_alert=True)
    chat_id = int(parts[1])
    client_id = int(parts[2])
    user = ubot._ubot[client_id]
    admin = await list_admins(user, chat_id)
    if callback_query.from_user.id not in admin:
        return await callback_query.answer("❌ Anda bukan admin group ini!", show_alert=True)
    perms_lock = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False,
        can_send_polls=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False
    )
    current_perms = await current_chat_permissions(user, chat_id)
    keyboard = create_locks_keyboard(current_perms, chat_id, client_id)
    try:
        await user.set_chat_permissions(chat_id, perms_lock)
        await update_locks_message(user, chat_id, callback_query, client_id)
        await callback_query.answer("🔒 Semua permission berhasil dikunci!", show_alert=True)
    except ChatNotModified:
        await callback_query.answer("⚠️ Semua permission sudah terkunci!", show_alert=True)
    except ChatAdminRequired:
        await callback_query.answer("❌ Anda tidak punya akses admin!", show_alert=True)
    except Exception as e:
        logger.exception(e)

# Unlock All
@USU.CALLBACK("bukaall_")
async def unlockall_callback(client, callback_query):
    parts = callback_query.data.split("_")
    if len(parts) < 3:
        return await callback_query.answer("❌ Invalid callback data!", show_alert=True)
    chat_id = int(parts[1])
    client_id = int(parts[2])
    user = ubot._ubot[client_id]
    admin = await list_admins(user, chat_id)
    if callback_query.from_user.id not in admin:
        return await callback_query.answer("❌ Anda bukan admin group ini!", show_alert=True)
    perms_unlock = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
        can_send_polls=True,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=False
    )
    current_perms = await current_chat_permissions(user, chat_id)
    keyboard = create_locks_keyboard(current_perms, chat_id, client_id)
    try:
        await user.set_chat_permissions(chat_id, perms_unlock)
        await update_locks_message(user, chat_id, callback_query, client_id)
        await callback_query.answer("🔓 Semua permission berhasil dibuka!", show_alert=True)
    except ChatNotModified:
        await callback_query.answer("⚠️ Semua permission sudah terbuka!", show_alert=True)
    except ChatAdminRequired:
        await callback_query.answer("❌ Anda tidak punya akses admin!", show_alert=True)
    except Exception as e:
        logger.exception(e)



@USU.UBOT("pin|unpin")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if not message.reply_to_message:
        return await message.edit(f"<b><i>{ggl}Reply text!</i></b>")
    r = message.reply_to_message
    await message.edit(f"<b><i>{prs}Processing...</i></b>")
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.edit(
            f"<b><i>{sks}Unpinned!</i></b>",
            disable_web_page_preview=True,
        )
    try:
        await r.pin(disable_notification=True)
        await message.edit(
            f"<b><i>{sks}Pinned!</i></b>",
            disable_web_page_preview=True,
        )
    except ChatAdminRequired:
        await message.edit(f"<b><i>{ggl}Not access!</i></b>")
        await message.delete()


@USU.UBOT("admin|fulladmin")
@USU.GROUP
async def _(client: Client, message: Message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    biji = await eor(message, f"<b><i>{prs}Processing...</i></b>")
    replied = message.reply_to_message
    usu = message.command
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
        
        if message.command[0] == "admin":
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
        elif message.command[0] == "fulladmin":
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


@USU.UBOT("unadmin")
@USU.GROUP
async def _(client: Client, message: Message):
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


@USU.UBOT("kick|ban|mute|unmute|unban")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(client.me.id, "inline")
    if message.command[0] == "kick":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        if user_id in DEVS:
            return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
        if user_id in (await list_admins(client, message.chat.id)):
            return await message.reply_text(
                f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_kick = f"""<b><i>{sks}Success kick {user_id}</i></b>"""
        try:
            await message.chat.ban_member(user_id)
            await message.reply(msg_kick)
            await asyncio.sleep(1)
            await message.chat.unban_member(user_id)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "ban":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        if user_id in DEVS:
            return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
        if user_id in (await list_admins(client, message.chat.id)):
            return await message.reply_text(
                f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_ban = f"""<b><i>{sks}Success ban {user_id}</i></b>"""
        try:
            await message.chat.ban_member(user_id)
            if vars:
                x = await client.get_inline_bot_results(bot.me.username, f"unban {id(message)} {user_id} {msg_ban}")
                if not x.results:
                    await message.reply(msg_ban)
                else:
                    await message.reply_inline_bot_result(x.query_id, x.results[0].id)
            else:
                await message.reply(msg_ban)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "mute":
        user_id, reason = await extract_user_and_reason(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        if user_id in DEVS:
            return await message.reply_text(f"<b><i>{ggl}Dia pemilik bot!</i></b>")
        if user_id in (await list_admins(client, message.chat.id)):
            return await message.reply_text(
                f"<b><i>{ggl}Dia adalah admin group ini!</i></b>"
            )
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        msg_mute = f"""<b><i>{sks}Success mute {user_id}</i></b>"""
        try:
            await message.chat.restrict_member(user_id, ChatPermissions())
            if vars:
                x = await client.get_inline_bot_results(bot.me.username, f"unmute {id(message)} {user_id} {msg_mute}")
                if not x.results:
                    await message.reply(msg_mute)
                else:
                    await message.reply_inline_bot_result(x.query_id, x.results[0].id)
            else:
                await message.reply(msg_mute)
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unmute":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b><i>{sks}Success unmute {user_id}</i></b>")
        except Exception as error:
            await message.reply(error)
    elif message.command[0] == "unban":
        user_id = await extract_user(message)
        if not user_id:
            return await message.reply_text(f"<b><i>{ggl}Pengguna tidak ditemukan!</i></b>")
        try:
            mention = (await client.get_users(user_id)).mention
        except Exception as error:
            await message.reply(error)
        try:
            await message.chat.unban_member(user_id)
            await message.reply(f"<b><i>{sks}Success unban {user_id}</i></b>")
        except Exception as error:
            await message.reply(error)

@USU.INLINE("unban|unmute")
async def inline_voicechat(client, inline_query):
    args = inline_query.query.split(None, 3)
    m = int(args[1])
    target_id = int(args[2])
    text = args[3]
    try:
        if args[0] == "unban":
            results = [
                InlineQueryResultArticle(
                    title="Unban",
                    input_message_content=InputTextMessageContent(text),
                    reply_markup=InlineKeyboardMarkup(
                        BTN.UNBAN(m, target_id)
                    ),
                )
            ]
        else:
            results = [
                InlineQueryResultArticle(
                    title="Unmute",
                    input_message_content=InputTextMessageContent(text),
                    reply_markup=InlineKeyboardMarkup(
                    BTN.UNMUTE(m, target_id)
                    ),
                )
            ]
        await inline_query.answer(results=results)
    except (BotResponseTimeout, QueryIdInvalid):
        pass
    except Exception as e:
        logger.exception(e)


@USU.CALLBACK("unban|unmute")
async def cancel_broadcast(client, callback_query):
    args = callback_query.data.split(maxsplit=2)
    c = next((target for target in get_objects() if id(target) == int(args[1])), None)
    tujuan = int(args[2])
    if callback_query.from_user.id != c._client.me.id:
        return await callback_query.answer(f"❌ Tombol ini bukan untuk anda!", True)
    if args[0] == "unban":
        await c.chat.unban_member(tujuan)
        return await callback_query.answer(f"✅ Berhasil melepas banned!", True)
    else:
        await c.chat.unban_member(tujuan)
        return await callback_query.answer(f"✅ Berhasil melepas bisu!", True)


@USU.UBOT("zombies")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    chat_id = message.chat.id
    deleted_users = []
    banned_users = 0
    Tm = await message.reply(f"<b><i>{prs}Processing...</i></b>")
    try:
        async for i in client.get_chat_members(chat_id):
            if i.user.is_deleted and i.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                deleted_users.append(i.user.id)
        if len(deleted_users) > 0:
            for deleted_user in deleted_users:
                try:
                    await client.ban_chat_member(chat_id, deleted_user)
                    banned_users += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await client.ban_chat_member(chat_id, deleted_user)
                    banned_users += 1
                except Exception as e:
                    pass
            await Tm.edit(f"<b><i>{sks}Success kick {banned_users} accounts deleted!</i></b>")
        else:
            await Tm.edit(f"<b><i>{ggl}No accounts deleted!</i></b>")
    except ChatAdminRequired:
        return await Tm.edit(f"<b><i>{ggl}Not access!</i></b>")
    except Exception as e:
        return await Tm.edit(e)
