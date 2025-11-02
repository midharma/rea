import os
import wget
import asyncio
from datetime import timedelta
from time import time
from youtubesearchpython import VideosSearch

from pyrogram import *


from usu import *





@USU.UBOT("vsong")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) < 2:
        return await message.reply_text(
            f"<i><b>{ggl}Video title not found!</b></i>",
        )
    infomsg = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<i><b>{ggl}Error!</b></i>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await infomsg.edit(f"<i><b>{ggl}Error!</b></i>")
    thumbnail = wget.download(thumb)
    await client.send_video(
        message.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "Video",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
        ),
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            "<i><b>{prs}Downloader...</b></i>",
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@USU.UBOT("song")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) < 2:
        return await message.reply_text(
            f"<i><b>{ggl}Audio title not found!</b></i>",
        )
    infomsg = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()[
            "result"
        ][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<i><b>{ggl}Error!</b></i>")
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await infomsg.edit(f"<i><b>{ggl}Error!</b></i>")
    thumbnail = wget.download(thumb)
    await client.send_audio(
        message.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "Audio",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
        ),
        progress=progress,
        progress_args=(
            infomsg,
            time(),
            "<i><b>{prs}Downloader...</b></i>",
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)