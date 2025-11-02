import asyncio
import os
from time import time
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from pyrogram import types as tipes
from usu import *

@USU.UBOT("copy")
async def copy_ubot_msg(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = message.reply_to_message or message
    infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    link = get_arg(message)
    if not (msg or link):
        return await infomsg.edit(f"<i><b>{ggl}<code>{message.text}</code> [link or reply]</b></i>")
    thumbs = None
    if link.startswith(("https", "t.me")):
        msg_id = int(link.split("/")[-1].split("?")[0])
        if "t.me/c/" in link:
            chat = int("-100" + str(link.split("/")[-2]))
            try:
                pv = await client.get_messages(chat, int(msg_id))
                try:
                    if pv.media_group_id:
                        hasil_media = []
                        sampahnya = []
                        medianya = await client.get_media_group(chat, pv.id)
                        for target in medianya:
                            file_path = await client.download_media(target)
                            sampahnya.append(file_path)
                            if target.video:
                                thumbs = await client.download_media(target.video.thumbs[0])
                            if target.photo:
                                hasil_media.append(InputMediaPhoto(media=file_path, caption=target.caption, caption_entities=target.caption_entities))
                            elif target.video:
                                hasil_media.append(InputMediaVideo(media=file_path, caption=target.caption, thumb=thumbs, caption_entities=target.caption_entities))
                        if hasil_media:
                            await client.send_media_group(chat_id=message.chat.id, media=hasil_media)
                            await infomsg.delete()
                        if sampahnya:
                            for smph in sampahnya:
                                os.remove(smph)
                        if thumbs:
                            os.remove(thumbs)
                    elif pv.media:
                        value = pv.media.value
                        media = getattr(pv, value)
                        try:
                            dl = await client.download_media(media)
                            if value == 'video':
                                thumbs = await client.download_media(media.thumbs[0])
                                await getattr(client, f"send_video")(message.chat.id, dl, caption=pv.caption, thumb=thumbs, caption_entities=pv.caption_entities, reply_to_message_id=msg.id)
                            else:
                                await getattr(client, f"send_{value}")(message.chat.id, dl, caption=pv.caption, caption_entities=pv.caption_entities, reply_to_message_id=msg.id)
                            await infomsg.delete()
                            if dl:
                                os.remove(dl)
                            if thumbs:
                                os.remove(thumbs)
                        except AttributeError:
                            await infomsg.edit(f"<i><b>Invalid!</b></i>")
                        except Exception as media_error:
                            await infomsg.edit(f"Error media: {media_error}")
                    else:
                        await pv.copy(message.chat.id, reply_to_message_id=msg.id)
                        await infomsg.delete()
                except Exception as e:
                    await infomsg.edit(f"Error: {e}")
            except Exception as e:
                await infomsg.edit(f"Error: {e}")
        elif link.startswith(("https://t.me/", "t.me/")) and "/s/" in link:
            try:
                username = link.split("/")[3] if link.startswith("https://") else link.split("/")[1]
                story_id = link.split("/s/")[1]
                stories = await client.get_stories(username, story_ids=[int(story_id)])
                for story in stories:
                    if story.media:
                        value = story.media.value
                        media = getattr(story, value)
                        try:
                            dl = await client.download_media(media)
                            if value == 'video':
                                thumbs = await client.download_media(media.thumbs[0])
                                await getattr(client, f"send_video")(message.chat.id, dl, caption=story.caption, thumb=thumbs, caption_entities=story.caption_entities, reply_to_message_id=msg.id)
                            else:
                                await getattr(client, f"send_{value}")(message.chat.id, dl, caption=story.caption, caption_entities=story.caption_entities, reply_to_message_id=msg.id)
                            await infomsg.delete()
                            if dl:
                                os.remove(dl)
                            if thumbs:
                                os.remove(thumbs)
                        except AttributeError:
                            await infomsg.edit(f"<i><b>Invalid!</b></i>")
                        except Exception as media_error:
                            await infomsg.edit(f"Error media: {media_error}")
                    else:
                        await infomsg.edit("Media tidak ditemukan.")
            except Exception as e:
                await infomsg.edit(f"Error: {e}")
        else:
            chat = str(link.split("/")[-2])
            msg_id = int(link.split("/")[-1].split("?")[0])
            pv = await client.get_messages(chat, int(msg_id))
            try:
                if pv.media_group_id:
                    hasil_media = []
                    sampahnya = []
                    medianya = await client.get_media_group(chat, pv.id)
                    for target in medianya:
                        file_path = await client.download_media(target)
                        sampahnya.append(file_path)
                        if target.video:
                            thumbs = await client.download_media(target.video.thumbs[0])
                        if target.photo:
                            hasil_media.append(InputMediaPhoto(media=target.photo.file_id, caption=target.caption, caption_entities=target.caption_entities))
                        elif target.video:
                            hasil_media.append(InputMediaVideo(media=target.video.file_id, caption=target.caption, thumb=thumbs, caption_entities=target.caption_entities))
                    if hasil_media:
                        await client.send_media_group(chat_id=message.chat.id, media=hasil_media)
                        await infomsg.delete()
                    if sampahnya:
                        for smph in sampahnya:
                            os.remove(smph)
                    if thumbs:
                        os.remove(thumbs)
                elif pv.media:
                    value = pv.media.value
                    media = getattr(pv, value)
                    try:
                        dl = await client.download_media(media)
                        if value == 'video':
                            thumbs = await client.download_media(media.thumbs[0])
                            await getattr(client, f"send_video")(message.chat.id, dl, caption=pv.caption, thumb=thumbs, caption_entities=pv.caption_entities, reply_to_message_id=msg.id)
                        else:
                            await getattr(client, f"send_{value}")(message.chat.id, dl, caption=pv.caption, caption_entities=pv.caption_entities, reply_to_message_id=msg.id)
                        await infomsg.delete()
                        if dl:
                            os.remove(dl)
                        if thumbs:
                            os.remove(thumbs)
                    except AttributeError:
                        await infomsg.edit(f"<i><b>Invalid!</b></i>")
                    except Exception as media_error:
                        await infomsg.edit(f"Error media: {media_error}")
                else:
                    await pv.copy(message.chat.id, reply_to_message_id=msg.id)
                    await infomsg.delete()
            except Exception as e:
                await infomsg.edit(f"Error: {e}")
    else:
        try:
            if msg.reply_markup:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_send|{id(message)}"
                )
                await client.send_inline_bot_result(
                    message.chat.id, x.query_id, x.results[0].id
                )
            elif msg.media_group_id:
                hasil_media = []
                sampahnya = []
                medianya = await client.get_media_group(message.chat.id, msg.id)
                for target in medianya:
                    file_path = await client.download_media(target)
                    sampahnya.append(file_path)
                    if target.video:
                        thumbs = await client.download_media(target.video.thumbs[0])
                    if target.photo:
                        hasil_media.append(InputMediaPhoto(media=target.photo.file_id, caption=target.caption, caption_entities=target.caption_entities))
                    elif target.video:
                        hasil_media.append(InputMediaVideo(media=target.video.file_id, caption=target.caption, thumb=thumbs, caption_entities=target.caption_entities))
                if hasil_media:
                    await client.send_media_group(chat_id=message.chat.id, media=hasil_media)
                if sampahnya:
                    for smph in sampahnya:
                        os.remove(smph)
                if thumbs:
                    os.remove(thumbs)
            elif msg.media:
                value = msg.media.value
                media = getattr(msg, value)
                dl = await client.download_media(media)
                if value == 'video':
                    thumbs = await client.download_media(media.thumbs[0])
                    await getattr(client, f"send_video")(message.chat.id, dl, caption=msg.caption, thumb=thumbs, caption_entities=msg.caption_entities, reply_to_message_id=msg.id)
                else:
                    await getattr(client, f"send_{value}")(message.chat.id, dl, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=msg.id)
                if dl:
                    os.remove(dl)
                if thumbs:
                    os.remove(thumbs)
            else:
                await msg.copy(message.chat.id, reply_to_message_id=msg.id)
            await infomsg.delete()
        except Exception as e:
            await infomsg.edit(f"Error: {e}")




@USU.UBOT("send")
async def _(client, message):
    thumbs = None
    if message.reply_to_message:
        chat_id = (
            message.chat.id if len(message.command) < 2 else message.text.split()[1]
        )
        try:
            if message.reply_to_message.reply_markup:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_send|{id(message)}"
                )
                return await client.send_inline_bot_result(
                    chat_id, x.query_id, x.results[0].id
                )
            elif message.reply_to_message.media_group_id:
                hasil_media = []
                sampahnya = []
                medianya = await client.get_media_group(message.chat.id, message.reply_to_message.id)
                for target in medianya:
                    file_path = await client.download_media(target)
                    sampahnya.append(file_path)
                    if target.video:
                        thumbs = await client.download_media(target.video.thumbs[0])
                    if target.photo:
                        hasil_media.append(InputMediaPhoto(media=target.photo.file_id, caption=target.caption, caption_entities=target.caption_entities))
                    elif target.video:
                        hasil_media.append(InputMediaVideo(media=target.video.file_id, caption=target.caption, thumb=thumbs, caption_entities=target.caption_entities))
                if hasil_media:
                    await client.send_media_group(chat_id=message.chat.id, media=hasil_media)
                if sampahnya:
                    for smph in sampahnya:
                        os.remove(smph)
                if thumbs:
                    os.remove(thumbs)
            elif message.reply_to_message.media:
                try:
                    pv = message.reply_to_message
                    if pv.media:
                        value = pv.media.value
                        media = getattr(pv, value)
                        try:
                            dl = await client.download_media(media)
                            if value == 'video':
                                thumbs = await client.download_media(media.thumbs[0])
                                await getattr(client, f"send_video")(message.chat.id, dl, caption=pv.caption, thumb=thumbs, caption_entities=pv.caption_entities, reply_to_message_id=msg.id)
                            else:
                                await getattr(client, f"send_{value}")(message.chat.id, dl, caption=pv.caption, caption_entities=pv.caption_entities, reply_to_message_id=message.reply_to_message.id)
                            if dl:
                                os.remove(dl)
                            if thumbs:
                                os.remove(thumbs)
                        except AttributeError:
                            await message.reply(f"<i><b>Invalid!</b></i>")
                except Exception as e:
                    await message.reply(str(e))
            else:
                return await message.reply_to_message.copy(chat_id)
        except Exception as e:
            await message.reply(str(e))
    else:
        if len(message.command) < 3:
            return await message.reply(f"<b><i>Invalid!</i></b>")
        chat_id, chat_text = message.text.split(None, 2)[1:]
        try:
            if "_" in chat_id:
                msg_id, to_chat = chat_id.split("_")
                return await client.send_message(
                    to_chat, chat_text, reply_to_message_id=int(msg_id)
                )
            else:
                return await client.send_message(chat_id, chat_text)
        except Exception as t:
            return await message.reply(f"{t}")




@USU.INLINE("get_send")
async def _(client, inline_query):
    _id = int(inline_query.query.split("|")[1])
    m = next((obj for obj in get_objects() if id(obj) == _id), None)
    if m.reply_to_message:
        msg = m.reply_to_message
        if msg.media:
            value = msg.media.value
            media = getattr(msg, value)
            file_id = getattr(media, "file_id")
            res = f"InlineQueryResultCached{value.capitalize()}"
            tipe = f"{value}_file_id"
            targetnya = getattr(tipes, res)
            results = [
                targetnya(
                    title="get send!",
                    description="copy inline",
                    reply_markup=msg.reply_markup,
                    caption=msg.caption,
                    caption_entities=msg.caption_entities,
                    **{tipe: file_id},
                )
            ]
            await inline_query.answer(results=results)
        elif msg.text:
            results = [
                InlineQueryResultArticle(
                    title="get send!",
                    description="copy inline",
                    reply_markup=msg.reply_markup,
                    input_message_content=InputTextMessageContent(
                        msg.text,
                        entities=msg.entities,
                    ),
                )
            ]
            await inline_query.answer(results=results)