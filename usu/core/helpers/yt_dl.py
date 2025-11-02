import math
import wget
import os
import asyncio

from pyrogram.errors import FloodWait, MessageNotModified
from youtubesearchpython import VideosSearch

from datetime import timedelta
from time import time

from asyncio import get_event_loop
from functools import partial

from yt_dlp import YoutubeDL
from usu.core.helpers.tools import run_sync

from usu import *



def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "kb", 2: "mb", 3: "gb", 4: "tb"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}"


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(days)} Hari, " if days else "")
        + (f"{str(hours)} Jam, " if hours else "")
        + (f"{str(minutes)} Menit, " if minutes else "")
        + (f"{str(seconds)} Detik, " if seconds else "")
        + (f"{str(milliseconds)} Mikrodetik, " if milliseconds else "")
    )
    return tmp[:-2]


async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("•" for _ in range(math.floor(percentage / 10))),
            "".join("~" for _ in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nEstimasi: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    f"""
<b>{type_of_ps}</b>

<b>File Id:</b> <code>{file_name}</code>

<b>{tmp}</b>
"""
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit(f"{type_of_ps}\n{tmp}")
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


cookies_usu = os.path.join(os.getcwd(), "usu", "cookies.txt")

async def YoutubeDownload(url, as_video=False):
    os.makedirs("downloads", exist_ok=True)

    if as_video:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": cookies_usu,
        }
    else:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
            "cookiefile": cookies_usu,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192",
            }],
        }

    ydl = YoutubeDL(ydl_opts)
    info = await asyncio.to_thread(ydl.extract_info, url, download=True)

    file_name = ydl.prepare_filename(info)

    if not as_video:
        file_name = os.path.splitext(file_name)[0] + ".m4a"

    return (
        file_name,
        info["title"],
        f"https://youtu.be/{info['id']}",
        info["duration"],
        f"{info['view_count']:,}".replace(",", "."),
        info["uploader"],
        f"https://img.youtube.com/vi/{info['id']}/hqdefault.jpg",
        "<i><b>Information {}</b>\n\n<b>Name:</b> {}<b>\n<b>Duration:</b> {}\n<b>View:</b> {}\n<b>Channel:</b> {}\n<b>Tautan:</b> <a href={}>YouTube</a></i>",
    )