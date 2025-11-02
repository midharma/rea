import asyncio
import random
from random import shuffle
from datetime import datetime
from usu.core.helpers.tools import run_sync

from usu import *
from usu.core.function.auto_tagall import tagallgcid, pesan, tagall_task

@USU.CALLBACK("^mention")
async def _(c, cq):
    button = BTN.TAMBAH()
    pesan = f"""<i><b>Halo,
Saya adalah menu [TagAll/Mention]({PHOTO})

Command:</b>
/all - tag semua orang
/stop - berhenti tag semua orang

<b>Command AutoTagAll Patner:</b>
/addpt id_group_patner - format_jam - text_pesan_tagall
/delpt id_group/username
/listpt menampilkan semua daftar patner tagall
/clearpt menghapus semua daftar patner tagall

<b>Example AutoTagAll Patner:</b>
/addpt @{GROUP} 19:00 Kata2 tagall

<b>Note:</b>
Tagall berhenti selama 5 menit
Format jam mengikuti jam WIB
Format username bisa berupa id group atau link group
Format text tagall bebas</i>"""
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))



emoji_categories = {
    "smileys": [
        "😀",
        "😃",
        "😄",
        "😁",
        "😆",
        "😅",
        "😂",
        "🤣",
        "😊",
        "😍",
        "🥰",
        "😘",
        "😎",
        "🥳",
        "😇",
        "🙃",
        "😋",
        "😛",
        "🤪",
    ],
    "animals": [
        "🐶",
        "🐱",
        "🐰",
        "🐻",
        "🐼",
        "🦁",
        "🐸",
        "🦊",
        "🦔",
        "🦄",
        "🐢",
        "🐠",
        "🐦",
        "🦜",
        "🦢",
        "🦚",
        "🦓",
        "🐅",
        "🦔",
    ],
    "food": [
        "🍎",
        "🍕",
        "🍔",
        "🍟",
        "🍩",
        "🍦",
        "🍓",
        "🥪",
        "🍣",
        "🍔",
        "🍕",
        "🍝",
        "🍤",
        "🥗",
        "🥐",
        "🍪",
        "🍰",
        "🍫",
        "🥤",
    ],
    "nature": [
        "🌲",
        "🌺",
        "🌞",
        "🌈",
        "🌊",
        "🌍",
        "🍁",
        "🌻",
        "🌸",
        "🌴",
        "🌵",
        "🍃",
        "🍂",
        "🌼",
        "🌱",
        "🌾",
        "🍄",
        "🌿",
        "🌳",
    ],
    "travel": [
        "✈️",
        "🚀",
        "🚲",
        "🚗",
        "⛵",
        "🏔️",
        "🚁",
        "🚂",
        "🏍️",
        "🚢",
        "🚆",
        "🛴",
        "🛸",
        "🛶",
        "🚟",
        "🚈",
        "🛵",
        "🛎️",
        "🚔",
    ],
    "sports": [
        "⚽",
        "🏀",
        "🎾",
        "🏈",
        "🎱",
        "🏓",
        "🥊",
        "⛳",
        "🏋️",
        "🏄",
        "🤸",
        "🏹",
        "🥋",
        "🛹",
        "🥏",
        "🎯",
        "🥇",
        "🏆",
        "🥅",
    ],
    "music": ["🎵", "🎶", "🎤", "🎧", "🎼", "🎸", "🥁", "🎷", "🎺", "🎻", "🪕", "🎹", "🔊"],
    "celebration": ["🎉", "🎊", "🥳", "🎈", "🎁", "🍰", "🧁", "🥂", "🍾", "🎆", "🎇"],
    "work": ["💼", "👔", "👓", "📚", "✏️", "📆", "🖥️", "🖊️", "📂", "📌", "📎"],
    "emotions": ["❤️", "💔", "😢", "😭", "😠", "😡", "😊", "😃", "🙄", "😳", "😇", "😍"],
}


def emoji_random():
    random_category = random.choice(tuple(emoji_categories.keys()))
    return random.choice(emoji_categories[random_category])



async def tagall_bots_task(client, message):
    global tagall_task
    chat_id = message.chat.id
    client_id = client.me.id

    # init dict
    if client_id not in tagall_task:
        tagall_task[client_id] = {}

    # cek task sudah berjalan
    if chat_id in tagall_task[client_id]:
        return

    # buat task
    task = asyncio.create_task(tagall_bots(client, message))
    tagall_task[client_id][chat_id] = task

    # bersihkan saat selesai
    def done_callback(fut):
        try:
            del tagall_task[client_id][chat_id]
        except KeyError:
            pass

    task.add_done_callback(done_callback)



# wrapper untuk tagall inline
async def tagall_inline_task(client, message):
    global tagall_task
    chat_id = message.chat.id
    client_id = client.me.id

    # init dict
    if client_id not in tagall_task:
        tagall_task[client_id] = {}

    # cek task sudah berjalan
    if chat_id in tagall_task[client_id]:
        return

    # buat task
    task = asyncio.create_task(tagall_inline(client, message))
    tagall_task[client_id][chat_id] = task

    # bersihkan saat selesai
    def done_callback(fut):
        try:
            del tagall_task[client_id][chat_id]
        except KeyError:
            pass

    task.add_done_callback(done_callback)

# wrapper untuk tagall original
async def tagall_ori_task(client, message):
    global tagall_task
    chat_id = message.chat.id
    client_id = client.me.id

    if client_id not in tagall_task:
        tagall_task[client_id] = {}

    if chat_id in tagall_task[client_id]:
        return

    task = asyncio.create_task(tagall_ori(client, message))
    tagall_task[client_id][chat_id] = task

    def done_callback(fut):
        try:
            del tagall_task[client_id][chat_id]
        except KeyError:
            pass

    task.add_done_callback(done_callback)

# ------------------- CANCEL TASK -------------------
async def cancel_tagall_task(client_id, chat_id):
    global tagall_task
    if client_id in tagall_task and chat_id in tagall_task[client_id]:
        task = tagall_task[client_id][chat_id]
        task.cancel()
        try:
            del tagall_task[client_id][chat_id]
        except KeyError:
            pass

async def tagall_inline(client, message):
    msg_id = id(message)
    chat_id = message.chat.id
    global tagallgcid, pesan
    if client.me.id not in tagallgcid:
        tagallgcid[client.me.id] = []
    if chat_id in tagallgcid[client.me.id]:
        return await message.reply("⚠️ TagAll sudah berjalan!")

    tagallgcid[client.me.id].append(chat_id)
    if client.me.id not in pesan:
        pesan[client.me.id] = {}
    if chat_id not in pesan[client.me.id]:
        pesan[client.me.id][chat_id] = []
    pesan[client.me.id][chat_id].append(message.id)
    users = []
    async for member in client.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue

        # Stop jika di-cancel
        if chat_id not in tagallgcid[client.me.id]:
            break

        mention = f"<a href=tg://user?id={member.user.id}>{member.user.first_name}</a>"
        users.append(mention)

        if len(users) == 5:
            batch = ", ".join(users)
            x = await client.get_inline_bot_results(bot.me.username, f"tagall {msg_id} {batch}")
            try:
                msg = await message.reply_inline_bot_result(
                    x.query_id,
                    x.results[0].id,
                    quote=False
                )
                pesan[client.me.id][chat_id].append(msg.updates[0].id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                msg = await message.reply_inline_bot_result(
                    x.query_id,
                    x.results[0].id,
                    quote=False
                )
                pesan[client.me.id][chat_id].append(msg.updates[0].id)
            await asyncio.sleep(2.5)
            users = []

    # Batch terakhir
    if users:
        batch = ", ".join(users)
        x = await client.get_inline_bot_results(bot.me.username, f"tagall {msg_id} {batch}")
        try:
            msg = await message.reply_inline_bot_result(
                x.query_id,
                x.results[0].id,
                quote=False
            )
            pesan[client.me.id][chat_id].append(msg.updates[0].id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            x = await client.get_inline_bot_results(bot.me.username, f"tagall {msg_id} {batch}")
            msg = await message.reply_inline_bot_result(
                x.query_id,
                x.results[0].id,
                quote=False
            )
            pesan[client.me.id][chat_id].append(msg.updates[0].id)
        await asyncio.sleep(2.5)

    # Bersihkan flag
    try:
        tagallgcid[client.me.id].remove(chat_id)
    except Exception:
        pass

    if client.me.id in pesan and message.chat.id in pesan[client.me.id]:
        await asyncio.sleep(60)
        try:
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)
        except Exception:
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)


async def tagall_ori(client, message):
    chat_id = message.chat.id
    global tagallgcid, pesan
    if client.me.id not in tagallgcid:
        tagallgcid[client.me.id] = []
    if chat_id in tagallgcid[client.me.id]:
        return await message.reply("⚠️ TagAll sudah berjalan!")
    text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else (
        message.reply_to_message.text if message.reply_to_message else ""
    )
    m = message.reply_to_message if message.reply_to_message else message
    tagallgcid[client.me.id].append(chat_id)
    if client.me.id not in pesan:
        pesan[client.me.id] = {}
    if chat_id not in pesan[client.me.id]:
        pesan[client.me.id][chat_id] = []
    pesan[client.me.id][chat_id].append(message.id)
    users = []
    async for member in client.get_chat_members(chat_id):
        if member.user.is_bot or member.user.is_deleted:
            continue

        # Stop jika di-cancel
        if chat_id not in tagallgcid[client.me.id]:
            break

        mention = f"<a href=tg://user?id={member.user.id}>{member.user.first_name}</a>"
        users.append(mention)

        if len(users) == 5:
            batch = ", ".join(users)
            try:
                msg = await m.reply_text(f"{text}\n\n<b>{batch}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
                pesan[client.me.id][chat_id].append(msg.id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                msg = await m.reply_text(f"{text}\n\n<b>{batch}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
                pesan[client.me.id][chat_id].append(msg.id)
            await asyncio.sleep(2.5)
            users = []

    # Batch terakhir
    if users:
        batch = ", ".join(users)
        try:
            msg = await m.reply_text(f"{text}\n\n<b>{batch}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
            pesan[client.me.id][chat_id].append(msg.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            msg = await m.reply_text(f"{text}\n\n<b>{batch}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>", quote=False)
            pesan[client.me.id][chat_id].append(msg.id)
        await asyncio.sleep(2.5)

    # Bersihkan flag
    try:
        tagallgcid[client.me.id].remove(chat_id)
    except Exception:
        pass

    if client.me.id in pesan and message.chat.id in pesan[client.me.id]:
        await asyncio.sleep(60)
        try:
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)
        except Exception:
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)

@USU.UBOT("tagall|all")
@USU.GROUP
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await tagall_inline_task(client, message)
    else:
        await tagall_ori_task(client, message)

# ------------------- INLINE HANDLER -------------------
@USU.INLINE("^tagall")
async def tagall_inline_query(client, inline_query):
    args = inline_query.query.split(None, 2)
    m = next((target for target in get_objects() if id(target) == int(args[1])), None)
    batch = args[2]

    text = m.text.split(None, 1)[1] if len(m.text.split()) != 1 else (
        m.reply_to_message.text if m.reply_to_message else ""
    )

    results = [
        InlineQueryResultArticle(
            title="📢 TagAll",
            input_message_content=InputTextMessageContent(
                f"{text}\n\n<b>{batch}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>",
            ),
            reply_markup=InlineKeyboardMarkup(
                BTN.CANCEL_BTN_CLIENT(int(args[1]))
            ),
        )
    ]
    await inline_query.answer(results=results)


# CALLBACK HANDLER: cancel tagall
@USU.CALLBACK("^cancel_client")
async def _(client, callback_query):
    global tagallgcid, pesan
    args = callback_query.data.split(maxsplit=1)
    m = next((target for target in get_objects() if id(target) == int(args[1])), None) 
    user = m._client.me.id
    chat_id = m.chat.id
    user_id = callback_query.from_user.id
    admins = await list_admins(m._client, chat_id)
    if user_id not in admins or user_id != user:
        return await callback_query.answer("⚠️ Anda tidak memiliki akses.", show_alert=True)
    try:
        if user in tagallgcid and chat_id in tagallgcid[user]:
            await callback_query.answer("✅ TagAll dihentikan!", show_alert=True)
            await cancel_tagall_task(user, chat_id)
            tagallgcid[user].remove(chat_id)
            if user in pesan and chat_id in pesan[user]:
                await asyncio.sleep(60)
                try:
                    for msg_id in pesan[user][chat_id]:
                        await ubot._ubot[user].delete_messages(chat_id, msg_id)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    for msg_id in pesan[user][chat_id]:
                        await ubot._ubot[user].delete_messages(chat_id, msg_id)
                except Exception:
                    for msg_id in pesan[user][chat_id]:
                        await ubot._ubot[user].delete_messages(chat_id, msg_id)
        else:
            await callback_query.answer("⚠️ Tidak ada TagAll yang berjalan.", show_alert=True)
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)

@USU.UBOT("cancel")
@USU.GROUP
async def _(client, message):
    global tagallgcid, pesan
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if client.me.id not in tagallgcid or message.chat.id not in tagallgcid[client.me.id]:
        return await message.reply_text(
            f"<i><b>{ggl}No tags all!</b></i>"
        )
    try:
        await cancel_tagall_task(client.me.id, message.chat.id)
        tagallgcid[client.me.id].remove(message.chat.id)
    except Exception:
        pass
    await message.reply_text(f"<i><b>{sks}Successfully canceled!</b></i>")
    if client.me.id in pesan and message.chat.id in pesan[client.me.id]:
        await asyncio.sleep(60)
        try:
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)
        except Exception:
            for msg_id in pesan[client.me.id][message.chat.id]:
                await client.delete_messages(message.chat.id, msg_id)


@USU.BOT("all|tagall")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    await tagall_bots_task(client, message)


async def tagall_bots(client, message):
    global tagallgcid, pesan
    if bot.me.id not in tagallgcid:
        tagallgcid[bot.me.id] = []
    if message.chat.id in tagallgcid[bot.me.id]:
        return

    tagallgcid[bot.me.id].append(message.chat.id)

    text = message.text.split(None, 1)[1] if len(message.text.split()) != 1 else (
        message.reply_to_message.text if message.reply_to_message else ""
    )
    m = message.reply_to_message if message.reply_to_message else message

    if message.chat.id not in pesan:
        pesan[message.chat.id] = []
    pesan[message.chat.id].append(message.id)
    users = []
    async for member in client.get_chat_members(message.chat.id):
        if not (member.user.is_bot or member.user.is_deleted):
            # Stop kalau sudah di-cancel
            if message.chat.id not in tagallgcid[bot.me.id]:
                break

            nama = f"{member.user.first_name} {member.user.last_name or ''}".strip()
            targetnya = f"<a href=tg://user?id={member.user.id}>{nama}</a>"
            users.append(targetnya)

            if len(users) == 5:
                shuffle(users)
                anu = ", ".join(users)
                try:
                    msg = await m.reply_text(
                        f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>",
                        quote=False,
                        reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN())  # ⬅️ Inline button disini juga
                    )
                    pesan[message.chat.id].append(msg.id)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    msg = await m.reply_text(
                        f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>",
                        quote=False,
                        reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN())  # ⬅️ Inline button disini juga
                    )
                    pesan[message.chat.id].append(msg.id)
                await asyncio.sleep(2.5)
                users = []

    if users and message.chat.id in tagallgcid[bot.me.id]:
        shuffle(users)
        anu = ", ".join(users)
        try:
            msg = await m.reply_text(
                f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>",
                quote=False,
                reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN())   # ⬅️ Inline button di batch terakhir
            )
            pesan[message.chat.id].append(msg.id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            msg = await m.reply_text(
                f"{text}\n\n<b>{anu}</b>\n<b><blockquote>🛒 @{CHANNEL}</blockquote></b>",
                quote=False,
                reply_markup=InlineKeyboardMarkup(BTN.CANCEL_BTN())   # ⬅️ Inline button di batch terakhir
            )
            pesan[message.chat.id].append(msg.id)
        await asyncio.sleep(2.5)

    try:
        tagallgcid[bot.me.id].remove(message.chat.id)
    except Exception:
        pass
    if message.chat.id in pesan:
        await asyncio.sleep(60)
        try:
            for msg_id in pesan[message.chat.id]:
                await bot.delete_messages(message.chat.id, msg_id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            for msg_id in pesan[message.chat.id]:
                await bot.delete_messages(message.chat.id, msg_id)
        except Exception:
            for msg_id in pesan[message.chat.id]:
                await bot.delete_messages(message.chat.id, msg_id)


# Handler tombol cancel
@USU.CALLBACK("^cancel_tagall")
async def cancel_tagall_handler(client, cq):
    global tagallgcid, pesan
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id

    admins = await list_admins(client, chat_id)
    if user_id not in admins:
        return await cq.answer("⚠️ Anda tidak memiliki akses admin.", show_alert=True)

    if bot.me.id in tagallgcid and chat_id in tagallgcid[bot.me.id]:
        await cq.answer("✅ TagAll dibatalkan!", show_alert=True)
        try:
            await cancel_tagall_task(bot.me.id, chat_id)
            tagallgcid[bot.me.id].remove(chat_id)
        except Exception:
            pass
        if chat_id in pesan:
            await asyncio.sleep(60)
            try:
                for msg_id in pesan[chat_id]:
                    await bot.delete_messages(chat_id, msg_id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                for msg_id in pesan[chat_id]:
                    await bot.delete_messages(chat_id, msg_id)
            except Exception:
                for msg_id in pesan[chat_id]:
                    await bot.delete_messages(chat_id, msg_id)
    else:
        await cq.answer("⚠️ Tidak ada TagAll yang berjalan.", show_alert=True)



@USU.BOT("cancel|stop")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    global tagallgcid, pesan
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if bot.me.id not in tagallgcid or message.chat.id not in tagallgcid[bot.me.id]:
        return await message.reply_text(
            f"<i><b>{ggl}No tags all!</b></i>"
        )
    try:
        await cancel_tagall_task(bot.me.id, message.chat.id)
        tagallgcid[bot.me.id].remove(message.chat.id)
    except Exception:
        pass
    await message.reply_text(f"<i><b>{sks}Successfully canceled!</b></i>")
    if message.chat.id in pesan:
        await asyncio.sleep(60)
        try:
            for msg_id in pesan[message.chat.id]:
                await bot.delete_messages(message.chat.id, msg_id)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            for msg_id in pesan[message.chat.id]:
                await bot.delete_messages(message.chat.id, msg_id)
        except Exception:
            for msg_id in pesan[message.chat.id]:
                await bot.delete_messages(message.chat.id, msg_id)



@USU.BOT("addpt")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    try:
        _, chat_id, jam, *pesan = message.text.split(None, 3)
    except:
        return await message.reply(
            "<i><b>Contoh format:\n</b>/addpt id_group 12:00 pesan</i>"
        )

    try:
        datetime.strptime(jam, "%H:%M")
    except ValueError:
        return await message.reply(
            "<i><b>Format jam salah. Gunakan format maksimal 23:59</b></i>"
        )

    if message.reply_to_message and message.reply_to_message.text:
        pesan = message.reply_to_message.text
    elif pesan:
        pesan = " ".join(pesan)
    else:
        return await message.reply(f"<i><b>Pesan tidak ditemukan. Kirim lewat argumen atau reply.</b></i>")

    id_group = await extract_id(message, chat_id)
    if id_group is None:
        return await message.reply(f"<i><b>Group patner tidak valid! mohon langsung masukan id group/username jika ada.</b></i>")
    data_list = await db.get_list_from_vars(client.me.id, "auto_tagall") or []

    for item in data_list:
        if item["chat_id"] == message.chat.id:
            for entry in item["data"]:
                if entry["id_group"] == id_group:
                    return await message.reply("<i><b>ID Group tersebut sudah terdaftar sebelumnya.</b></i>")
            item["data"].append({"id_group": id_group, "jam": jam, "pesan": pesan})
            await db.set_vars(client.me.id, "auto_tagall", data_list)
            return await message.reply(
                f"<i><b>Berhasil menambahkan!</b>\nID Group: <code>{id_group}</code>\nJam: <b>{jam}</b>\nPesan: {pesan}</i>"
            )

    new_data = {
        "chat_id": message.chat.id,
        "data": [{"id_group": id_group, "jam": jam, "pesan": pesan}]
    }
    await db.add_to_vars(client.me.id, "auto_tagall", new_data)
    await message.reply(
        f"<i><b>Berhasil menambahkan!</b>\nID Group: <code>{id_group}</code>\nJam: <b>{jam}</b>\nPesan: {pesan}</i>"
    )

@USU.BOT("delpt")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    try:
        _, id_group = message.text.split(None, 1)
    except:
        return await message.reply("<i><b>Contoh:\n</b>/delpt id_group</i>")

    chat_id = await extract_id(message, id_group)
    data_list = await db.get_list_from_vars(client.me.id, "auto_tagall") or []

    if chat_id is None:
        return await message.reply(f"<i><b>Group patner tidak valid! mohon langsung masukan id group/username jika ada.</b></i>")
    for item in data_list:
        if item["chat_id"] == message.chat.id:
            if not any(d["id_group"] == chat_id for d in item["data"]):
                return await message.reply(
                    f"<i><b>ID Group <code>{id_group}</code> tidak ditemukan dalam daftar Auto TagAll grup ini.</b></i>"
                )
            item["data"] = [d for d in item["data"] if d["id_group"] != chat_id]
            break
    else:
        return await message.reply(
            f"<i><b>Tidak ada data Auto TagAll untuk grup ini.</b></i>"
        )

    await db.set_vars(client.me.id, "auto_tagall", data_list)
    await message.reply(
        f"<i><b>Semua entri dengan ID Group <code>{id_group}</code> telah dihapus.</b></i>"
    )


@USU.BOT("listpt")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    data_list = await db.get_list_from_vars(client.me.id, "auto_tagall") or []

    for item in data_list:
        if item["chat_id"] == message.chat.id:
            if not item["data"]:
                break
            text = "<b>📋 Daftar Patner:</b>\n\n"
            for i, d in enumerate(item["data"], 1):
                text += (
                    f"<b>{i}.</b> ID Group: <code>{d['id_group']}</code>\n"
                    f"⏰ {d['jam']}\n"
                    f"💬 {d['pesan']}\n\n"
                )
            return await message.reply(text)

    await message.reply("<b>📋 Daftar Patner:</b>\n\n<i>Belum ada data.</i>")

@USU.BOT("clearpt")
@USU.GROUP
@USU.ADMIN
async def _(client, message):
    data_list = await db.get_list_from_vars(client.me.id, "auto_tagall") or []
    for target in data_list:
        if target["chat_id"] == message.chat.id:
            await db.remove_from_vars(client.me.id, "auto_tagall", target)
            return await message.reply("<b><i>Semua partner auto tagall di grup ini telah dihapus.</i></b>")
    return await message.reply(f"<i><b>Grup ini tidak memiliki daftar partner auto tagall.</b></i>")