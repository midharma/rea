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

    if len(message.command) < 2:
        return await message.reply_text(f"<i><b>{ggl}Video title not found!</b></i>")

    query = message.text.split(None, 1)[1]
    infomsg = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")

    try:
        if query.startswith(("https", "t.me")):
            if "youtu.be" in query or "youtube.com" in query:
                link = query
        else:
            search = VideosSearch(query, limit=1).result()["result"][0]
            link = f"https://youtu.be/{search['id']}"
    except Exception as e:
        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

    try:
        # ubah ke as_video=True (karena ini video)
        file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
    except Exception as e:
        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

    # ambil id YouTube (backup kalau search tidak ada)
    yt_id = link.split("youtu.be/")[1] if "youtu.be" in link else link.split("v=")[1].split("&")[0]
    thumbnail = wget.download(thumb)

    try:
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
                f"<i><b>{prs}Downloader...</b></i>",
                f"{yt_id}.mp4",
            ),
            reply_to_message_id=message.id,
        )
    finally:
        # biar file tetap terhapus walaupun kirim gagal
        await infomsg.delete()
        for files in (thumbnail, file_name):
            if files and os.path.exists(files):
                os.remove(files)


@USU.UBOT("song")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)

    if len(message.command) < 2:
        return await message.reply_text(f"<i><b>{ggl}Audio title not found!</b></i>")

    query = message.text.split(None, 1)[1]
    infomsg = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")

    try:
        if query.startswith(("https", "t.me")):
            if "youtu.be" in query or "youtube.com" in query:
                link = query
        else:
            search = VideosSearch(query, limit=1).result()["result"][0]
            link = f"https://youtu.be/{search['id']}"
    except Exception as e:
        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

    try:
        # untuk audio
        file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
    except Exception as e:
        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

    yt_id = link.split("youtu.be/")[1] if "youtu.be" in link else link.split("v=")[1].split("&")[0]
    thumbnail = wget.download(thumb)

    try:
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
                f"<i><b>{prs}Downloader...</b></i>",
                f"{yt_id}.mp3",
            ),
            reply_to_message_id=message.id,
        )
    finally:
        await infomsg.delete()
        for files in (thumbnail, file_name):
            if files and os.path.exists(files):
                os.remove(files)