import wget

from gc import get_objects

from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent)

from usu import *
from pyrogram.errors import FloodWait



async def send_log(client, chat_id, message, message_text, msg):
    usu = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Message Link", url=f"{message.link}")]]
        if "LOGS_GROUP" in msg
        else [[InlineKeyboardButton("Message Link", url=f"tg://openmessage?user_id={message.from_user.id}&message_id={message.id}")]]
    )
    tmp_file = None
    send_text = getattr(bot, f"send_message", None)
    try:
        if message.media:
            media_type = message.media.value
            send_media = getattr(bot, f"send_{media_type}", None)

            if send_media:
                tmp_file = await client.download_media(getattr(message, media_type))

                kwargs = {"reply_markup": usu}
                if media_type in ["photo", "video", "document", "animation", "audio"]:
                    kwargs["caption"] = message_text
                    await send_media(chat_id, tmp_file, **kwargs)
                elif media_type == "sticker":
                    await send_text(chat_id, message_text, **kwargs)
                    await send_media(chat_id, tmp_file, **kwargs)
        else:
            await send_text(chat_id, message_text, reply_markup=usu)

        if tmp_file and os.path.exists(tmp_file):
            os.remove(tmp_file)
    except Exception as e:
        pass


@USU.UBOT("logger")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")

    value = query[command]

    await db.set_vars(client.me.id, "ON_LOGS", value)
    await message.reply(
        f"<i><b>{sks}Logger {value}</b></i>"
    )
    if command == "on":
        return await bot.send_message(client.me.id, f"<i><b>Logger on!</b></i>")
    else:
        return await bot.send_message(client.me.id, f"<i><b>Logger off!</b></i>")


@USU.NO_CMD("LOGS_PRIVATE", ubot)
async def _(client, message):
    user_link = f"{message.from_user.mention}" if message.from_user else f"{message.sender_chat.title}"
    user_id = f"{message.from_user.id}" if message.from_user else f"{message.sender_chat.id}"
    if message.photo or message.video or message.document or message.voice or message.audio or message.animation:
        message_text = f"""Information Private!
Name: {user_link}
ID: <code>{user_id}</code>

Chat Name: {message.chat.title}
Chat ID: <code>{message.chat.id}</code>
Chat Type: Private

Message ID: <code>{message.id}</code>
Message: {message.caption}"""
    else:
        message_text = f"""Information Private!
Name: {user_link}
ID: <code>{user_id}</code>

Chat Name: {message.chat.title}
Chat ID: <code>{message.chat.id}</code>
Chat Type: Private

Message ID: <code>{message.id}</code>
Message: {message.text}"""
    try:
        await send_log(client, client.me.id, message, f"<b><i>{message_text}</i></b>", "LOGS_PRIVATE")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await send_log(client, client.me.id, message, f"<b><i>{message_text}</i></b>", "LOGS_PRIVATE")
    except Exception as e:
        logger.exception(e)

@USU.NO_CMD("LOGS_GROUP", ubot)
async def _(client, message):
    user_link = f"{message.from_user.mention}" if message.from_user else f"{message.sender_chat.title}"
    user_id = f"{message.from_user.id}" if message.from_user else f"{message.sender_chat.id}"
    if message.photo or message.video or message.document or message.voice or message.audio or message.animation:
        message_text = f"""Information Group!
Name: {user_link}
ID: <code>{user_id}</code>

Chat Name: {message.chat.title}
Chat ID: <code>{message.chat.id}</code>
Chat Type: Group

Message ID: <code>{message.id}</code>
Message: {message.caption}"""
    else:
        message_text = f"""Information Group!
Name: {user_link}
ID: <code>{user_id}</code>

Chat Name: {message.chat.title}
Chat ID: <code>{message.chat.id}</code>
Chat Type: Group

Message ID: <code>{message.id}</code>
Message: {message.text}"""
    try:
        await send_log(client, client.me.id, message, f"<b><i>{message_text}</i></b>", "LOGS_GROUP")
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await send_log(client, client.me.id, message, f"<b><i>{message_text}</i></b>", "LOGS_GROUP")
    except Exception as e:
        logger.exception(e)


async def safe_send_reply(client, message, chat_id, reply_to_message_id):
    try:
        if message.media:
            media_type = message.media.value
            media_obj = getattr(message, media_type)
            send_func = getattr(client, f"send_{media_type}", None)

            if send_func:
                kwargs = {"reply_to_message_id": reply_to_message_id}

                if media_type in ["photo", "video", "document", "animation", "audio"]:
                    kwargs["caption"] = getattr(message, "caption", None)

                await send_func(chat_id, media_obj.file_id, **kwargs)
            else:
                await message.copy(chat_id, reply_to_message_id=reply_to_message_id)
        else:
            await message.copy(chat_id, reply_to_message_id=reply_to_message_id)

    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await safe_send_reply(client, message, chat_id, reply_to_message_id)
    except Exception as e:
        logger.exception(f"Error saat kirim reply: {e}")



@USU.NO_CMD("REPLY", ubot)
async def reply_to_log(client, message):
    if not message.reply_to_message:
        return

    # Ambil teks atau caption
    text = message.reply_to_message.text or message.reply_to_message.caption
    if not text:
        return

    # Ambil semua angka dari teks
    ids = re.findall(r"-?\d+", text)
    if len(ids) < 2:
        return  # minimal ada Chat ID dan Message ID

    # Ambil dua terakhir sebagai chat_id dan message_id
    chat_id = int(ids[-2])
    message_id = int(ids[-1])

    # Kirim reply
    await safe_send_reply(client, message, chat_id, message_id)