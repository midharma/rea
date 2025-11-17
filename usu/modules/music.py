import asyncio
from random import randint

from pytgcalls.types import *
from pytgcalls.exceptions import *
from youtubesearchpython import VideosSearch

from pyrogram import *
from pyrogram.types import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputPeerChannel, InputPeerChat
from pyrogram.errors import FloodWait, MessageNotModified, ChatAdminRequired, UserNotParticipant
from usu import *
from pyrogram.errors import ChatSendInlineForbidden, ChatSendMediaForbidden


loop = asyncio.get_event_loop()


@USU.CALLBACK("^music")
async def _(c, cq):
    button = BTN.TAMBAH()
    pesan = f"""<i><b>Halo,
Saya adalah menu [Music]({PHOTO})

Command Devs:</b>
/activevc - melihat semua chat yang sedang memainkan music
/setname - mengganti nama assistant music
/setbio - mengganti bio assistant music

<b>Command Admins:</b>
/play or /vplay - memutar music
/end - hentikan music
/skip - memutar antrian music
/resume - melanjutkan music
/pause - jeda music
/playlist - lihat daftar antrian music</i>"""
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))


playlist = {}
playtask = {}
paused = {}
waw = 0
orang = {}


@ubot.usu_stream()
async def _(client, update):
    chat_id = update.chat_id
    return await client.leave_call(chat_id)


@bot.usu_stream()
async def leave_and_play_next(client, update):
    chat_id = update.chat_id
    if not bot.assistant:
        return
    if chat_id in playlist and len(playlist[chat_id]) > 1:
        try:
            lagu_berikutnya = playlist[chat_id][1]['lagu']
            judul = playlist[chat_id][1]['judul']
            thumb = playlist[chat_id][1]['thumb']
            await client.play(chat_id, MediaStream(lagu_berikutnya))
            if thumb is not None:
                await bot.send_photo(chat_id, caption=f"""<i><b>Memutar antrian!</b>

{judul}</i>""", photo=thumb, reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
            else:
                await bot.send_message(chat_id, f"""<i><b>Memutar antrian!</b>

{judul}</i>""", reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
            bersihkan(lagu_berikutnya, thumb)
            if chat_id in playlist:
                playlist[chat_id].pop(0)
        except Exception as e:
            logger.exception(f"[Leave and Play Next Error] {e}")
    elif chat_id in playlist and len(playlist[chat_id]) == 1:
        try:
            file = playlist[chat_id][0]["lagu"]
            thumb = playlist[chat_id][0]["thumb"]
            bersihkan(file, thumb)
            await client.leave_call(chat_id)
            del playlist[chat_id]
        except NoActiveGroupCall:
            pass
        except Exception as e:
            logger.exception(f"[Leave Call Error] {e}")


async def gabung(usu, message):
    if FSUB:
        buttons = []
        anu = []
        for channel in FSUB:
            if message.sender_chat:
                continue
            try:
                await usu.get_chat_member(channel, message.from_user.id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await usu.get_chat_member(channel, message.from_user.id)
            except UserNotParticipant:
                try:
                    link = await usu.export_chat_invite_link(channel)
                    anu.append(InlineKeyboardButton(f"Join", url=link))
                    if len(anu) == 2:
                        buttons.append(anu)
                        anu = []
                except Exception as e:
                    logger.exception(f"[Export Invite Link Error] {e}")
        if anu:
            buttons.append(anu)
        if buttons:
            kontol = InlineKeyboardMarkup(buttons)
            await message.reply_text(f"<b><i>Halo {message.from_user.mention},\nSilahkan bergabung terlebih dahulu ke Support chat!</i></b>", reply_markup=kontol)
            return False
    return True


@USU.UBOT("playlist")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")

    if client.me.id not in playlist or (client.me.id in playlist and message.chat.id not in playlist[client.me.id]):
        await anu.edit(f"<i><b>{ggl}Playlist kosong!</b></i>")
    else:
        text = f"<i><b>{broad}Sedang diputar:</b>\n{playlist[client.me.id][message.chat.id][0]['judul']}\n\n"
        if len(playlist[client.me.id][message.chat.id]) > 1:
            text += f"<b>{ptr}Daftar antrian:</b>\n"
            for i, lagu in enumerate(playlist[client.me.id][message.chat.id][1:], start=1):
                text += f"{i}. {lagu['judul']}\n\n"
        text += "</i>"
        await anu.edit(text)


def bersihkan(file, thumb):
    try:
        if file and os.path.exists(file):
            os.remove(file)
        if thumb and os.path.exists(thumb):
            os.remove(thumb)
    except Exception as e:
        logger.exception(f"[Bersihkan Error] {e}")


async def next_song(client, chat_id, duration):
    try:
        # Pastikan duration dalam detik
        if isinstance(duration, timedelta):
            duration = duration.total_seconds()
        
        await asyncio.sleep(duration)
        
        if client.me.id in playlist and chat_id in playlist[client.me.id] and len(playlist[client.me.id][chat_id]) > 1:
            lagu = playlist[client.me.id][chat_id][1]['lagu']
            dur_berikutnya = playlist[client.me.id][chat_id][1]['duration']
            thumb = playlist[client.me.id][chat_id][1]['thumb']
            judul = playlist[client.me.id][chat_id][1]['judul']
            
            if isinstance(dur_berikutnya, timedelta):
                dur_berikutnya = dur_berikutnya.total_seconds()

            await client.call_py.play(chat_id, MediaStream(lagu))
            bersihkan(lagu, thumb)
            playlist[client.me.id][chat_id].pop(0)
            
            # Kirim notifikasi
            sks = await EMO.SUKSES(client)
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username,
                    f"play|{client.me.id}|{chat_id}|<b>{sks}Memutar antrian!</b>"
                )
                await client.send_inline_bot_result(
                    chat_id,
                    x.query_id,
                    x.results[0].id,
                )
            except (ChatSendMediaForbidden, ChatSendInlineForbidden):
                await client.send_message(chat_id, f"<i><b>{sks}Memutar antrian!</b>\n\n{judul}</i>")
            except Exception as e:
                logger.exception(f"[Send Inline Result Error] {e}")
            
            if client.me.id not in playtask:
                playtask[client.me.id] = {}
            if client.me.id in playtask and chat_id in playtask[client.me.id]:
                task = playtask[client.me.id][chat_id]
                if not task.done():
                    task.cancel()
                del playtask[client.me.id][chat_id]
            
            playtask[client.me.id][chat_id] = loop.create_task(
                next_song(client, chat_id, dur_berikutnya)
            )
        elif client.me.id in playlist and chat_id in playlist[client.me.id] and len(playlist[client.me.id][chat_id]) == 1:
            file = playlist[client.me.id][chat_id][0]["lagu"]
            thumb = playlist[client.me.id][chat_id][0]["thumb"]
            bersihkan(file, thumb)
            await client.call_py.leave_call(chat_id)
            del playlist[client.me.id][chat_id]
            if client.me.id in playtask and chat_id in playtask[client.me.id]:
                task = playtask[client.me.id][chat_id]
                if not task.done():
                    task.cancel()
                del playtask[client.me.id][chat_id]
    except asyncio.CancelledError:
        logger.info(f"[Next Song] Task cancelled for chat {chat_id}")
    except Exception as e:
        logger.exception(f"[Next Song Error] {e}")


# =================== USU UBOT PLAY ===================
async def play_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    title = None
    file_name = None
    thumb = None
    duration = None
    views = None
    channel = None
    nama = None
    try:
        # ===== REPLY MESSAGE HANDLING =====
        if message.reply_to_message:
            media = (
                message.reply_to_message.audio
                if message.reply_to_message.audio
                else message.reply_to_message.voice
                if message.reply_to_message.voice
                else message.reply_to_message.video
            )
            teks = message.reply_to_message.text

            if teks:
                query = teks
                infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
                nama = "Audio"

            elif media:
                infomsg = await message.reply(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'}...</b></i>")

                async def progress(current, total):
                    percent = round((current / total) * 100)
                    global waw
                    if percent != waw:
                        waw = percent
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'} {percent}%...</b></i>")
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except Exception:
                            pass

                file_name = await client.download_media(media, progress=progress)
                nama = "Audio" if message.reply_to_message.audio else "Voice" if message.reply_to_message.voice else "Video"
                title = "None"
                duration = media.duration or 0
                channel = "Local Audio" if message.reply_to_message.audio else "Local Voice" if message.reply_to_message.voice else "Local Video"
                views = "N/A"
                thumb = await client.download_media(message.reply_to_message.video.thumbs[0]) if message.reply_to_message.video and message.reply_to_message.video.thumbs else None

        # ===== COMMAND TEXT HANDLING =====
        else:
            if len(message.command) < 2:
                return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

            query = message.text.split(None, 1)[1]
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")

            # LINK HANDLING
            if query.startswith(("https", "t.me")):
                # YouTube link
                if "youtu.be" in query or "youtube.com" in query:
                    nama = "Audio"
                    try:
                        file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(query, as_video=False)
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # t.me channel link
                elif "t.me/c/" in query:
                    msg_id = int(query.split("/")[-1])
                    chat = int("-100" + str(query.split("/")[-2]))
                    try:
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            nama = "Video"
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # Forwarded message from chat id/msg id
                else:
                    try:
                        chat = str(query.split("/")[-2])
                        msg_id = str(query.split("/")[-1])
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            nama = "Video"
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            # NORMAL TEXT → YouTube search
            else:
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
                nama = "Audio"

        chat_id = message.chat.id
        hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""
        
        if client.me.id not in orang:
            orang[client.me.id] = client
        if client.me.id not in playlist:
            playlist[client.me.id] = {}

        if client.me.id in playlist and chat_id in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})
            await infomsg.delete()
            hasil_text = f"<b>{sks}Ditambahkan ke antrian!</b>"
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username,
                    f"play|{client.me.id}|{message.chat.id}|{hasil_text}"
                )
                await message.reply_inline_bot_result(
                    x.query_id,
                    x.results[0].id,
                    quote=False
                )
            except (ChatSendMediaForbidden, ChatSendInlineForbidden):
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            return
            
        if message.chat.id not in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id] = []
            playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})
        
        hasil_text = f"<b>{sks}Memutar ke {nama}!</b>"
        try:
            await client.call_py.play(chat_id, MediaStream(file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p))
            bersihkan(file_name, thumb)
            if client.me.id not in playtask:
                playtask[client.me.id] = {}
            playtask[client.me.id][message.chat.id] = loop.create_task(next_song(client, message.chat.id, playlist[client.me.id][message.chat.id][0]['duration']))
            await infomsg.delete()
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username,
                    f"play|{client.me.id}|{message.chat.id}|{hasil_text}"
                )
                await message.reply_inline_bot_result(
                    x.query_id,
                    x.results[0].id,
                    quote=False
                )
            except (ChatSendMediaForbidden, ChatSendInlineForbidden):
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            except Exception as e:
                await message.reply(f"<b>{ggl}Error:</b> {str(e)}")
        except NoActiveGroupCall:
            await message.reply(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
        except Exception as e:
            await message.reply(f"<i><b>{ggl}Gagal mengirim inline result!</b></i>\n{str(e)}")
    except Exception as e:
        logger.exception(e)


async def play_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    title = None
    file_name = None
    thumb = None
    duration = None
    views = None
    channel = None
    nama = None
    try:
        # ===== REPLY MESSAGE HANDLING =====
        if message.reply_to_message:
            media = (
                message.reply_to_message.audio
                if message.reply_to_message.audio
                else message.reply_to_message.voice
                if message.reply_to_message.voice
                else message.reply_to_message.video
            )
            teks = message.reply_to_message.text

            if teks:
                query = teks
                infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
                nama = "Audio"

            elif media:
                infomsg = await message.reply(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'}...</b></i>")

                async def progress(current, total):
                    percent = round((current / total) * 100)
                    global waw
                    if percent != waw:
                        waw = percent
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'} {percent}%...</b></i>")
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except Exception:
                            pass

                file_name = await client.download_media(media, progress=progress)
                nama = "Audio" if message.reply_to_message.audio else "Voice" if message.reply_to_message.voice else "Video"
                title = "None"
                duration = media.duration or 0
                channel = "Local Audio" if message.reply_to_message.audio else "Local Voice" if message.reply_to_message.voice else "Local Video"
                views = "N/A"
                thumb = await client.download_media(message.reply_to_message.video.thumbs[0]) if message.reply_to_message.video and message.reply_to_message.video.thumbs else None

        # ===== COMMAND TEXT HANDLING =====
        else:
            if len(message.command) < 2:
                return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

            query = message.text.split(None, 1)[1]
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")

            # LINK HANDLING
            if query.startswith(("https", "t.me")):
                # YouTube link
                if "youtu.be" in query or "youtube.com" in query:
                    nama = "Audio"
                    try:
                        file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(query, as_video=False)
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # t.me channel link
                elif "t.me/c/" in query:
                    msg_id = int(query.split("/")[-1])
                    chat = int("-100" + str(query.split("/")[-2]))
                    try:
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            nama = "Video"
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # Forwarded message from chat id/msg id
                else:
                    try:
                        chat = str(query.split("/")[-2])
                        msg_id = str(query.split("/")[-1])
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            nama = "Video"
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            # NORMAL TEXT → YouTube search
            else:
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
                nama = "Audio"

        chat_id = message.chat.id
        hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""
        
        if client.me.id not in orang:
            orang[client.me.id] = client
        if client.me.id not in playlist:
            playlist[client.me.id] = {}

        if client.me.id in playlist and chat_id in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})
            await infomsg.delete()
            hasil_text = f"<b>{sks}Ditambahkan ke antrian!</b>"
            try:
                if thumb:
                    await message.reply_photo(photo=thumb, caption=f"<i>{hasil_text}\n\n{hasil}</i>", quote=False)
                else:
                    await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            except ChatSendMediaForbidden:
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            return
            
        if message.chat.id not in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id] = []
            playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})
        
        hasil_text = f"<b>{sks}Memutar ke {nama}!</b>"
        try:
            await client.call_py.play(chat_id, MediaStream(file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p))
            bersihkan(file_name, thumb)
            if client.me.id not in playtask:
                playtask[client.me.id] = {}
            playtask[client.me.id][message.chat.id] = loop.create_task(next_song(client, message.chat.id, playlist[client.me.id][message.chat.id][0]['duration']))
            await infomsg.delete()
            try:
                if thumb:
                    await message.reply_photo(photo=thumb, caption=f"<i>{hasil_text}\n\n{hasil}</i>", quote=False)
                else:
                    await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            except ChatSendMediaForbidden:
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
        except NoActiveGroupCall:
            await message.reply(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
        except Exception as e:
            await message.reply(f"<b>{ggl}Error:</b> {str(e)}")
    except Exception as e:
        logger.exception(e)


@USU.UBOT("play|vplay")
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if message.command[0].lower() == "play":
        if vars:
            await play_inline(client, message)
        else:
            await play_ori(client, message)
    else:
        if vars:
            await vplay_inline(client, message)
        else:
            await vplay_ori(client, message)


# =================== USU INLINE PLAY ===================
@USU.INLINE("play")
async def play_inline_result(client, inline_query):
    data = inline_query.query.split("|", 3)
    _client = int(data[1])
    chat_id = int(data[2])
    hasil_text = data[3]
    
    if _client not in playlist or chat_id not in playlist[_client] or not playlist[_client][chat_id]:
        return
    
    thumb = playlist[_client][chat_id][-1]['thumb']
    if _client in orang:
        anu = orang[_client]
        hasil = "<i>" + hasil_text + "\n\n" + playlist[_client][chat_id][-1]['judul'] + "</i>"
        if thumb:
            results = [
                InlineQueryResultPhoto(
                    photo_url=thumb,
                    caption=hasil,
                    title="Play Result",
                    reply_markup=InlineKeyboardMarkup(BTN.PLAY_CLIENT(_client, chat_id))
                )
            ]
        else:
            results = [
                InlineQueryResultArticle(
                    title="Play Result",
                    input_message_content=InputTextMessageContent(hasil),
                    reply_markup=InlineKeyboardMarkup(BTN.PLAY_CLIENT(_client, chat_id))
                )
            ]

        await inline_query.answer(results=results)


async def vplay_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    title = None
    file_name = None
    thumb = None
    duration = None
    views = None
    channel = None
    nama = "Video"
    try:
        # ===== REPLY MESSAGE HANDLING =====
        if message.reply_to_message:
            media = (
                message.reply_to_message.audio
                if message.reply_to_message.audio
                else message.reply_to_message.voice
                if message.reply_to_message.voice
                else message.reply_to_message.video
            )
            teks = message.reply_to_message.text

            if teks:
                query = teks
                infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            elif media:
                infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")

                async def progress(current, total):
                    percent = round((current / total) * 100)
                    global waw
                    if percent != waw:
                        waw = percent
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except Exception:
                            pass

                file_name = await client.download_media(media, progress=progress)
                title = "None"
                duration = media.duration or 0
                channel = "Local Video"
                views = "N/A"
                thumb = await client.download_media(message.reply_to_message.video.thumbs[0]) if message.reply_to_message.video and message.reply_to_message.video.thumbs else None

        # ===== COMMAND TEXT HANDLING =====
        else:
            if len(message.command) < 2:
                return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

            query = message.text.split(None, 1)[1]
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")

            if query.startswith(("https", "t.me")):
                # YouTube link
                if "youtu.be" in query or "youtube.com" in query:
                    try:
                        file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(query, as_video=True)
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # t.me channel link
                elif "t.me/c/" in query:
                    msg_id = int(query.split("/")[-1])
                    chat = int("-100" + str(query.split("/")[-2]))
                    try:
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # Forwarded message from chat id/msg id
                else:
                    try:
                        chat = str(query.split("/")[-2])
                        msg_id = str(query.split("/")[-1])
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            else:
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

        chat_id = message.chat.id
        hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""

        if client.me.id not in orang:
            orang[client.me.id] = client
        if client.me.id not in playlist:
            playlist[client.me.id] = {}

        if client.me.id in playlist and chat_id in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})
            await infomsg.delete()
            hasil_text = f"<b>{sks}Ditambahkan ke antrian!</b>"
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username,
                    f"play|{client.me.id}|{message.chat.id}|{hasil_text}"
                )
                await message.reply_inline_bot_result(
                    x.query_id,
                    x.results[0].id,
                    quote=False
                )
            except (ChatSendMediaForbidden, ChatSendInlineForbidden):
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            return

        if message.chat.id not in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id] = []
        playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})

        hasil_text = f"<b>{sks}Memutar ke {nama}!</b>"
        try:
            await client.call_py.play(chat_id, MediaStream(file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p))
            bersihkan(file_name, thumb)
            if client.me.id not in playtask:
                playtask[client.me.id] = {}
            playtask[client.me.id][message.chat.id] = loop.create_task(next_song(client, message.chat.id, playlist[client.me.id][message.chat.id][0]['duration']))
            await infomsg.delete()
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username,
                    f"play|{client.me.id}|{message.chat.id}|{hasil_text}"
                )
                await message.reply_inline_bot_result(
                    x.query_id,
                    x.results[0].id,
                    quote=False
                )
            except (ChatSendMediaForbidden, ChatSendInlineForbidden):
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            except Exception as e:
                await message.reply(f"<b>{ggl}Error:</b> {str(e)}")
        except NoActiveGroupCall:
            await message.reply(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
        except Exception as e:
            await message.reply(f"<i><b>{ggl}Gagal mengirim inline result!</b></i>\n{str(e)}")
    except Exception as e:
        logger.exception(e)


async def vplay_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    title = None
    file_name = None
    thumb = None
    duration = None
    views = None
    channel = None
    nama = "Video"
    try:
        # ===== REPLY MESSAGE HANDLING =====
        if message.reply_to_message:
            media = (
                message.reply_to_message.audio
                if message.reply_to_message.audio
                else message.reply_to_message.voice
                if message.reply_to_message.voice
                else message.reply_to_message.video
            )
            teks = message.reply_to_message.text

            if teks:
                query = teks
                infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            elif media:
                infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")

                async def progress(current, total):
                    percent = round((current / total) * 100)
                    global waw
                    if percent != waw:
                        waw = percent
                        try:
                            await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except Exception:
                            pass

                file_name = await client.download_media(media, progress=progress)
                title = "None"
                duration = media.duration or 0
                channel = "Local Video"
                views = "N/A"
                thumb = await client.download_media(message.reply_to_message.video.thumbs[0]) if message.reply_to_message.video and message.reply_to_message.video.thumbs else None

        # ===== COMMAND TEXT HANDLING =====
        else:
            if len(message.command) < 2:
                return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

            query = message.text.split(None, 1)[1]
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")

            if query.startswith(("https", "t.me")):
                # YouTube link
                if "youtu.be" in query or "youtube.com" in query:
                    try:
                        file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(query, as_video=True)
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # t.me channel link
                elif "t.me/c/" in query:
                    msg_id = int(query.split("/")[-1])
                    chat = int("-100" + str(query.split("/")[-2]))
                    try:
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

                # Forwarded message from chat id/msg id
                else:
                    try:
                        chat = str(query.split("/")[-2])
                        msg_id = str(query.split("/")[-1])
                        pv = await client.get_messages(chat, int(msg_id))
                        if pv.video:
                            async def progress(current, total):
                                percent = round((current / total) * 100)
                                global waw
                                if percent != waw:
                                    waw = percent
                                    try:
                                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                    except FloodWait as e:
                                        await asyncio.sleep(e.value)
                                    except Exception:
                                        pass

                            file_name = await client.download_media(pv.video, progress=progress)
                            title = "None"
                            duration = pv.video.duration or 0
                            channel = "Local Video"
                            views = "N/A"
                            thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                    except Exception as e:
                        return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            else:
                try:
                    search_result = VideosSearch(query, limit=1).result()["result"][0]
                    link = f"https://youtu.be/{search_result['id']}"
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

        chat_id = message.chat.id
        hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}"""

        if client.me.id not in orang:
            orang[client.me.id] = client
        if client.me.id not in playlist:
            playlist[client.me.id] = {}

        if client.me.id in playlist and chat_id in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})
            await infomsg.delete()
            hasil_text = f"<b>{sks}Ditambahkan ke antrian!</b>"
            try:
                if thumb:
                    await message.reply_photo(photo=thumb, caption=f"<i>{hasil_text}\n\n{hasil}</i>", quote=False)
                else:
                    await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            except ChatSendMediaForbidden:
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            return

        if message.chat.id not in playlist[client.me.id]:
            playlist[client.me.id][message.chat.id] = []
        playlist[client.me.id][message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb, "duration": timedelta(seconds=duration)})

        hasil_text = f"<b>{sks}Memutar ke {nama}!</b>"
        try:
            await client.call_py.play(chat_id, MediaStream(file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p))
            bersihkan(file_name, thumb)
            if client.me.id not in playtask:
                playtask[client.me.id] = {}
            playtask[client.me.id][message.chat.id] = loop.create_task(next_song(client, message.chat.id, playlist[client.me.id][message.chat.id][0]['duration']))
            await infomsg.delete()
            try:
                if thumb:
                    await message.reply_photo(photo=thumb, caption=f"<i>{hasil_text}\n\n{hasil}</i>", quote=False)
                else:
                    await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
            except ChatSendMediaForbidden:
                await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
        except NoActiveGroupCall:
            await message.reply(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
        except Exception as e:
            await message.reply(f"<b>{ggl}Error:</b> {str(e)}")

    except Exception as e:
        logger.exception(e)


@USU.UBOT("end")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    chat_id = message.chat.id
    
    if client.me.id in paused and chat_id in paused[client.me.id]:
        del paused[client.me.id][chat_id]
    if chat_id not in playlist.get(client.me.id, {}):
        return await message.reply(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")
    if client.me.id in playlist and chat_id in playlist[client.me.id]:
        del playlist[client.me.id][chat_id]
    if client.me.id in playtask and chat_id in playtask[client.me.id]:
        task = playtask[client.me.id][chat_id]
        if not task.done():
            task.cancel()
        del playtask[client.me.id][chat_id]
    if client.me.id in orang:
        del orang[client.me.id]
    try:
        await client.call_py.leave_call(chat_id)
        return await message.reply(f"<i><b>{sks}Streaming end!</b></i>")      
    except Exception as e:
        return await message.reply(f"<b>{ggl}Error:</b> {str(e)}")


@USU.UBOT("pause")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id

    if chat_id not in playlist.get(client.me.id, {}):
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if client.me.id not in paused:
        paused[client.me.id] = {}

    if chat_id in paused[client.me.id]:
        return await anu.edit(f"<i><b>{ggl}Streaming sudah dalam keadaan pause!</b></i>")

    try:
        await client.call_py.pause_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-pause!</b></i>")
        paused[client.me.id][chat_id] = True
        if client.me.id in playtask and chat_id in playtask[client.me.id]:
            task = playtask[client.me.id][chat_id]
            if not task.done():
                task.cancel()
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {str(e)}")


@USU.UBOT("resume")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id

    if chat_id not in playlist.get(client.me.id, {}):
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if client.me.id in paused and chat_id not in paused[client.me.id]:
        return await anu.edit(f"<i><b>{ggl}Streaming sedang tidak di-pause!</b></i>")
    try:
        await client.call_py.resume_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-resume!</b></i>")
        del paused[client.me.id][chat_id]
        if client.me.id not in playtask:
            playtask[client.me.id] = {}
        playtask[client.me.id][chat_id] = loop.create_task(
            next_song(client, chat_id, playlist[client.me.id][chat_id][0]['duration'])
        )
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {str(e)}")


@USU.UBOT("skip")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id

    # Hapus status pause jika ada
    if client.me.id in paused and chat_id in paused[client.me.id]:
        del paused[client.me.id][chat_id]

    # Cek kalau ada playlist dan ada antrian lebih dari 1
    if client.me.id in playlist and chat_id in playlist[client.me.id] and len(playlist[client.me.id][chat_id]) > 1:
        if client.me.id in playtask and chat_id in playtask[client.me.id]:
            task = playtask[client.me.id][chat_id]
            if not task.done():
                task.cancel()

        try:
            # Ambil lagu berikut (index 1)
            next_track = playlist[client.me.id][chat_id][1]
            current_track = playlist[client.me.id][chat_id][0]

            # Mainkan lagu berikut
            await client.call_py.play(chat_id, MediaStream(next_track['lagu']))

            # Bersihkan lagu sebelumnya, bukan yang baru!
            bersihkan(current_track['lagu'], current_track['thumb'])

            # Hapus lagu lama dari playlist
            playlist[client.me.id][chat_id].pop(0)

            # Buat task auto-next
            playtask[client.me.id][chat_id] = loop.create_task(
                next_song(client, chat_id, next_track['duration'])
            )

        except Exception as e:
            return await anu.edit(f"<b>{ggl}Error:</b> {str(e)}")
    else:
        return await anu.edit(f"<i><b>{ggl}Tidak ada antrian streaming!</b></i>")

    await anu.delete()

    hasil = playlist[client.me.id][chat_id][0]["judul"]
    hasil_text = f"""<b>{sks}Memutar antrian!</b>"""

    try:
        x = await client.get_inline_bot_results(
            bot.me.username,
            f"play|{client.me.id}|{chat_id}|{hasil_text}"
        )
        await message.reply_inline_bot_result(
            x.query_id,
            x.results[0].id,
            quote=False
        )
    except (ChatSendMediaForbidden, ChatSendInlineForbidden):
        await message.reply(f"<i>{hasil_text}\n\n{hasil}</i>")
    except Exception as e:
        await message.reply(f"<b>{ggl}Error:</b> {str(e)}")



# =================== BOT COMMANDS ===================


@USU.BOT("playlist")
@USU.GC
async def _(client, message):
    if not bot.assistant:
        return
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    
    if message.chat.id not in playlist:
        await anu.edit(f"<i><b>{ggl}Playlist kosong!</b></i>")
    else:
        text = f"<i><b>{broad}Sedang diputar:</b>\n{playlist[message.chat.id][0]['judul']}\n\n"
        if len(playlist[message.chat.id]) > 1:
            text += f"<b>{ptr}Daftar antrian:</b>\n"
            for i, lagu in enumerate(playlist[message.chat.id][1:], start=1):
                text += f"{i}. {lagu['judul']}\n\n"
        text += "</i>"
        await anu.edit(text)


@USU.BOT("play")
@USU.GC
async def _(client, message):
    if not bot.assistant:
        return
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
        if message.chat.id not in group:
            await db.add_to_vars(bot.me.id, "group", message.chat.id)
    else:
        if message.chat.id not in channel:
            await db.add_to_vars(bot.me.id, "channel", message.chat.id)
    
    if FSUB:
        if not await gabung(client, message):
            return
    
    if message.reply_to_message:
        media = message.reply_to_message.audio if message.reply_to_message.audio else message.reply_to_message.voice if message.reply_to_message.voice else message.reply_to_message.video
        teks = message.reply_to_message.text
        
        if teks:
            query = teks
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
            nama = "Audio"
            
        elif media:
            infomsg = await message.reply(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'}...</b></i>")
            
            async def progress(current, total):
                percent = round((current / total) * 100)
                global waw
                if percent != waw:
                    waw = percent
                    try:
                        await infomsg.edit(f"<i><b>{prs}Downloading {'Audio' if message.reply_to_message.audio else 'Voice' if message.reply_to_message.voice else 'Video'} {percent}%...</b></i>")
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except Exception:
                        pass
                        
            file_name = await client.download_media(media, progress=progress)
            nama = "Audio" if message.reply_to_message.audio else "Voice" if message.reply_to_message.voice else "Video"
            title = "None"
            duration = media.duration or 0
            channel = "Local Audio" if message.reply_to_message.audio else "Local Voice" if message.reply_to_message.voice else "Local Video"
            views = "N/A" 
            thumb = await client.download_media(message.reply_to_message.video.thumbs[0]) if message.reply_to_message.video and message.reply_to_message.video.thumbs else None
    else:
        if len(message.command) < 2:
            return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

        query = message.text.split(None, 1)[1]
        if query.startswith(("https", "t.me")):
            if "youtu.be" in query or "youtube.com" in query:
                nama = "Audio"
                infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
                try:
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(str(query), as_video=False)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
            elif "t.me/c/" in query:
                msg_id = int(query.split("/")[-1])
                chat = int("-100" + str(query.split("/")[-2]))
                try:
                    pv = await client.get_messages(chat, int(msg_id))
                    if pv.video:
                        infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                        async def progress(current, total):
                            percent = round((current / total) * 100)
                            global waw
                            if percent != waw:
                                waw = percent
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except Exception:
                                    pass
                        file_name = await client.download_media(pv.video, progress=progress)
                        nama = "Video"
                        title = "None"
                        duration = pv.video.duration or 0
                        channel = "Local Video"
                        views = "N/A"
                        thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                except Exception as e:
                    return await message.reply(f"<b>{ggl}Error:</b> {str(e)}")
            else:
                try:
                    chat = str(query.split("/")[-2])
                    msg_id = str(query.split("/")[-1])
                    pv = await client.get_messages(chat, int(msg_id))
                    if pv.video:
                        infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                        async def progress(current, total):
                            percent = round((current / total) * 100)
                            global waw
                            if percent != waw:
                                waw = percent
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except Exception:
                                    pass
                        file_name = await client.download_media(pv.video, progress=progress)
                        nama = "Video"
                        title = "None"
                        duration = pv.video.duration or 0
                        channel = "Local Video"
                        views = "N/A"
                        thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                except Exception as e:
                    return await message.reply(f"<b>{ggl}Error:</b> {str(e)}")
        else:
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=False)
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
            nama = "Audio"

    chat_id = message.chat.id
    if message.from_user:
        jepret = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    else:
        jepret = f"{message.sender_chat.title}"
    hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}
<b>Requested By:</b> {jepret}"""
    
    try:
        try:
            get = await client.get_chat_member(message.chat.id, bot.usu.me.id)
        except ChatAdminRequired:
            return await infomsg.edit(f"<b><i>Mohon berikan izin admin yang cukup!</i></b>")
        if (get.status == ChatMemberStatus.BANNED or get.status == ChatMemberStatus.RESTRICTED):
            username_ass = f"@{bot.usu.me.username}" if bot.usu.me.username else ""
            return await infomsg.edit(f"<b><i>Mohon unbanned Assistant Music!\nUsername: {username_ass}\nID: {bot.usu.me.id}</i></b>")
    except UserNotParticipant:
        try:
            chat = await client.get_chat(message.chat.id)
            if chat.invite_link:
                await bot.usu.join_chat(chat.invite_link)
            else:
                export_link = await client.export_chat_invite_link(message.chat.id)
                await bot.usu.join_chat(export_link)
        except ChatAdminRequired:
            return await infomsg.edit(f"<b><i>Mohon berikan izin admin yang cukup!</i></b>")
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(message.chat.id, bot.usu.me.id)
            except Exception as e:
                logger.exception(f"[Approve Join Request Error] {e}")
        except Exception as e:
            logger.exception(f"[Join Chat Error] {e}")
    except Exception as e:
        logger.exception(f"[Get Chat Member Error] {e}")
    
    try:
        await message.delete()
    except Exception as e:
        bersihkan(file_name, thumb)
        return await infomsg.edit(f"<b><i>Mohon berikan hak admin yang cukup!</i></b>")
    
    if chat_id in playlist:
        playlist[message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb})
        await infomsg.delete()
        if thumb is not None:
            return await message.reply_photo(caption=f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""", photo=thumb, reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
        else:
            return await message.reply(f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""", reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
    
    if chat_id not in playlist:
        playlist[message.chat.id] = []
        playlist[message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb})
    
    try:
        await infomsg.delete()
        await bot.assistant.play(chat_id, MediaStream(
            file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p
        ))
        bersihkan(file_name, thumb)
        if thumb is not None:
            await message.reply_photo(caption=f"""<i><b>{sks}Memutar {nama}!</b>

{hasil}</i>
""", photo=thumb, reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
        else:
            await message.reply(f"""<i><b>{sks}Memutar {nama}!</b>

{hasil}</i>
""", reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply(f"""<i><b>{sks}Memutar {nama}!</b>

{hasil}</i>
""", reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
    except NoActiveGroupCall:
        await message.reply(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
    except Exception as e:
        await message.reply(f"<b>{ggl}Error:</b> {str(e)}")


@USU.BOT("vplay")
@USU.GC
async def _(client, message):
    if not bot.assistant:
        return
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
        if message.chat.id not in group:
            await db.add_to_vars(bot.me.id, "group", message.chat.id)
    else:
        if message.chat.id not in channel:
            await db.add_to_vars(bot.me.id, "channel", message.chat.id)
    
    if FSUB:
        if not await gabung(client, message):
            return
    
    if message.reply_to_message:
        media = message.reply_to_message.video
        teks = message.reply_to_message.text
        
        if teks:
            query = teks
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
                
        elif media:
            infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
            async def progress(current, total):
                percent = round((current / total) * 100)
                global waw
                if percent != waw:
                    waw = percent
                    try:
                        await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except Exception:
                        pass
            file_name = await client.download_media(media, progress=progress)
            title = "None"
            duration = media.duration or 0
            channel = "Local Video"
            views = "N/A"
            thumb = await client.download_media(message.reply_to_message.video.thumbs[0]) if message.reply_to_message.video and message.reply_to_message.video.thumbs else None
    else:
        if len(message.command) < 2:
            return await message.reply(f"<i><b>{ggl}Mohon berikan judul yang kamu inginkan!!</b></i>")

        query = message.text.split(None, 1)[1]
        if query.startswith(("https", "t.me")):
            if "youtu.be" in query or "youtube.com" in query:
                infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
                try:
                    file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(str(query), as_video=True)
                except Exception as e:
                    return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")
            elif "t.me/c/" in query:
                msg_id = int(query.split("/")[-1])
                chat = int("-100" + str(query.split("/")[-2]))
                try:
                    pv = await client.get_messages(chat, int(msg_id))
                    if pv.video:
                        infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                        async def progress(current, total):
                            percent = round((current / total) * 100)
                            global waw
                            if percent != waw:
                                waw = percent
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except Exception:
                                    pass
                        file_name = await client.download_media(pv.video, progress=progress)
                        title = "None"
                        duration = pv.video.duration or 0
                        channel = "Local Video"
                        views = "N/A"
                        thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                except Exception as e:
                    return await message.reply(f"<b>{ggl}Error:</b> {str(e)}")
            else:
                try:
                    chat = str(query.split("/")[-2])
                    msg_id = str(query.split("/")[-1])
                    pv = await client.get_messages(chat, int(msg_id))
                    if pv.video:
                        infomsg = await message.reply(f"<i><b>{prs}Downloading Video...</b></i>")
                        async def progress(current, total):
                            percent = round((current / total) * 100)
                            global waw
                            if percent != waw:
                                waw = percent
                                try:
                                    await infomsg.edit(f"<i><b>{prs}Downloading Video {percent}%...</b></i>")
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except Exception:
                                    pass
                        file_name = await client.download_media(pv.video, progress=progress)
                        title = "None"
                        duration = pv.video.duration or 0
                        channel = "Local Video"
                        views = "N/A"
                        thumb = await client.download_media(pv.video.thumbs[0]) if pv.video.thumbs else None
                except Exception as e:
                    return await message.reply(f"<b>{ggl}Error:</b> {str(e)}")
        else:
            infomsg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
            try:
                search_result = VideosSearch(query, limit=1).result()["result"][0]
                link = f"https://youtu.be/{search_result['id']}"
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

            try:
                file_name, title, url, duration, views, channel, thumb, data_ytp = await YoutubeDownload(link, as_video=True)
            except Exception as e:
                return await infomsg.edit(f"<b>{ggl}Error:</b> {str(e)}")

    chat_id = message.chat.id
    if message.from_user:
        jepret = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    else:
        jepret = f"{message.sender_chat.title}"
    hasil = f"""<b>Title:</b> {title}
<b>Duration:</b> {timedelta(seconds=duration)}
<b>Views:</b> {views}
<b>Channel:</b> {channel}
<b>Requested By:</b> {jepret}"""
    
    try:
        try:
            get = await client.get_chat_member(message.chat.id, bot.usu.me.id)
        except ChatAdminRequired:
            return await infomsg.edit(f"<b><i>Mohon berikan izin admin yang cukup!</i></b>")
        if (get.status == ChatMemberStatus.BANNED or get.status == ChatMemberStatus.RESTRICTED):
            username_ass = f"@{bot.usu.me.username}" if bot.usu.me.username else ""
            return await infomsg.edit(f"<b><i>Mohon unbanned Assistant Music!\nUsername: {username_ass}\nID: {bot.usu.me.id}</i></b>")
    except UserNotParticipant:
        try:
            chat = await client.get_chat(message.chat.id)
            if chat.invite_link:
                await bot.usu.join_chat(chat.invite_link)
            else:
                export_link = await client.export_chat_invite_link(message.chat.id)
                await bot.usu.join_chat(export_link)
        except ChatAdminRequired:
            return await infomsg.edit(f"<b><i>Mohon berikan izin admin yang cukup!</i></b>")
        except InviteRequestSent:
            try:
                await client.approve_chat_join_request(message.chat.id, bot.usu.me.id)
            except Exception as e:
                logger.exception(f"[Approve Join Request Error] {e}")
        except Exception as e:
            logger.exception(f"[Join Chat Error] {e}")
    except Exception as e:
        logger.exception(f"[Get Chat Member Error] {e}")
    
    try:
        await message.delete()
    except Exception as e:
        bersihkan(file_name, thumb)
        return await infomsg.edit(f"<b><i>Mohon berikan hak admin yang cukup!</i></b>")

    if chat_id in playlist:
        playlist[message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb})
        await infomsg.delete()
        if thumb is not None:
            return await message.reply_photo(caption=f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""", photo=thumb, reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
        else:
            return await message.reply(f"""<i><b>{sks}Ditambahkan ke antrian!</b>

{hasil}</i>
""", reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
    
    if chat_id not in playlist:
        playlist[message.chat.id] = []
        playlist[message.chat.id].append({"judul": hasil, "lagu": file_name, "thumb": thumb})
    
    try:
        await infomsg.delete()
        await bot.assistant.play(chat_id, MediaStream(file_name, audio_parameters=AudioQuality.STUDIO, video_parameters=VideoQuality.FHD_1080p))
        bersihkan(file_name, thumb)
        if thumb is not None:
            await message.reply_photo(caption=f"""<i><b>{sks}Memutar Video!</b>

{hasil}</i>
""", photo=thumb, reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
        else:
            await message.reply(f"""<i><b>{sks}Memutar Video!</b>

{hasil}</i>
""", reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply(f"""<i><b>{sks}Memutar Video!</b>

{hasil}</i>
""", reply_markup=InlineKeyboardMarkup(BTN.PLAY()))
    except NoActiveGroupCall:
        await message.reply(f"<i><b>{ggl}Voice chat tidak aktif, mohon aktifkan voice chat!</b></i>")
    except Exception as e:
        await message.reply(f"<b>{ggl}Error:</b> {str(e)}")


@USU.BOT("end")
@USU.GC
@USU.ADMIN
async def _(client, message):
    if not bot.assistant:
        return
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    chat_id = message.chat.id
    
    if message.from_user:
        jepret = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    else:
        jepret = f"{message.sender_chat.title}"
    
    try:
        await message.delete()
    except Exception as e:
        return await message.reply(f"<b><i>Mohon berikan hak admin yang cukup!</i></b>")
    
    if chat_id in paused:
        del paused[chat_id]
    if chat_id not in playlist:
        return await message.reply(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")
    if chat_id in playlist:
        del playlist[message.chat.id]
    try:
        await bot.assistant.leave_call(chat_id)
        return await message.reply(f"<i><b>{sks}Streaming end by {jepret}</b></i>")      
    except Exception as e:
        return await message.reply(f"<b>{ggl}Error:</b> {str(e)}")


@USU.BOT("pause")
@USU.GC
@USU.ADMIN
async def _(client, message):
    if not bot.assistant:
        return
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    
    if message.from_user:
        jepret = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    else:
        jepret = f"{message.sender_chat.title}"
    
    try:
        await message.delete()
    except Exception as e:
        return await anu.edit(f"<b><i>Mohon berikan hak admin yang cukup!</i></b>")
    
    if chat_id not in playlist:
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if chat_id in paused:
        return await anu.edit(f"<i><b>{ggl}Streaming sudah dalam keadaan pause!</b></i>")

    try:
        await bot.assistant.pause_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-pause by {jepret}</b></i>")
        paused[chat_id] = True
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {str(e)}")


@USU.BOT("resume")
@USU.GC
@USU.ADMIN
async def _(client, message):
    if not bot.assistant:
        return
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id
    
    if message.from_user:
        jepret = f"{message.from_user.first_name} {message.from_user.last_name or ''}"
    else:
        jepret = f"{message.sender_chat.title}"
    
    try:
        await message.delete()
    except Exception as e:
        return await anu.edit(f"<b><i>Mohon berikan hak admin yang cukup!</i></b>")
    
    if chat_id not in playlist:
        return await anu.edit(f"<i><b>{ggl}Tidak ada streaming yang aktif!</b></i>")

    if chat_id not in paused:
        return await anu.edit(f"<i><b>{ggl}Streaming sedang tidak di-pause!</b></i>")

    try:
        await bot.assistant.resume_stream(chat_id)
        await anu.edit(f"<i><b>{sks}Streaming di-resume by {jepret}</b></i>")
        del paused[chat_id]
    except Exception as e:
        return await anu.edit(f"<b>{ggl}Error:</b> {str(e)}")


@USU.BOT("skip")
@USU.GC
@USU.ADMIN
async def _(client, message):
    if not bot.assistant:
        return

    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    anu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    chat_id = message.chat.id

    try:
        await message.delete()
    except Exception:
        return await anu.edit("<b><i>Mohon berikan hak admin yang cukup!</i></b>")

    # hapus status paused bila ada
    if chat_id in paused:
        del paused[chat_id]

    # cek apakah ada antrian berikutnya
    if chat_id in playlist and len(playlist[chat_id]) > 1:
        next_song = playlist[chat_id][1]

        try:
            # mainkan lagu berikutnya (JANGAN bersihkan di sini)
            await bot.assistant.play(chat_id, MediaStream(next_song["lagu"]))
        except Exception as e:
            return await anu.edit(f"<b>{ggl}Error:</b> {str(e)}")

        # hapus lagu sebelumnya dari antrian SETELAH berhasil skip
        playlist[chat_id].pop(0)

        await anu.delete()

        # tampilkan info lagu baru
        if next_song["thumb"]:
            await message.reply_photo(
                caption=f"""<i><b>{sks}Memutar antrian!</b>\n\n{next_song['judul']}</i>""",
                photo=next_song["thumb"],
                reply_markup=InlineKeyboardMarkup(BTN.PLAY()),
            )
        else:
            await message.reply(
                f"""<i><b>{sks}Memutar antrian!</b>\n\n{next_song['judul']}</i>""",
                reply_markup=InlineKeyboardMarkup(BTN.PLAY()),
            )

    else:
        await anu.edit(f"<i><b>{ggl}Tidak ada antrian streaming!</b></i>")



# =================== CALLBACK MUSIC ===================

@USU.CALLBACK("pause")
async def pause(c, cq):
    if cq.from_user:
        jepret = f"{cq.from_user.first_name} {cq.from_user.last_name or ''}"
    else:
        jepret = f"{cq.message.sender_chat.title}"
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    
    admin = await list_admins(c, cq.message.chat.id)
    if user_id not in admin and user_id not in DEVS:
        return await cq.answer(f"Tombol ini untuk admin!", True)

    if chat_id not in playlist:
        return await cq.answer(f"Tidak ada streaming yang aktif!", True)

    if chat_id in paused:
        return await cq.answer(f"Streaming sudah dalam keadaan pause!", True)
    
    try:
        await bot.assistant.pause_stream(chat_id)
        await bot.send_message(chat_id, f"<i><b>Streaming di-pause by {jepret}</b></i>")
        await cq.answer(f"Streaming di-pause!", True)
        paused[chat_id] = True
    except Exception as e:
        await cq.answer(f"Error: {str(e)}", True)


@USU.CALLBACK("resume")
async def resume(c, cq):
    if cq.from_user:
        jepret = f"{cq.from_user.first_name} {cq.from_user.last_name or ''}"
    else:
        jepret = f"{cq.message.sender_chat.title}"
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    
    admin = await list_admins(c, cq.message.chat.id)
    if user_id not in admin and user_id not in DEVS:
        return await cq.answer(f"Tombol ini untuk admin!", True)

    if chat_id not in playlist:
        return await cq.answer(f"Tidak ada streaming yang aktif!", True)

    if chat_id not in paused:
        return await cq.answer(f"Streaming sedang tidak di-pause!", True)
    await c.assistant.resume_stream(chat_id)
    await bot.send_message(chat_id, f"<i><b>Streaming di-resume by {jepret}</b></i>")
    await cq.answer(f"Streaming di-resume!", True)
    del paused[chat_id]

@USU.CALLBACK("skip")
async def skip(c, cq):
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    admin = await list_admins(c, chat_id)
    
    # Validasi siapa yang bisa tekan tombol
    if user_id not in admin and user_id not in DEVS:
        return await cq.answer("Tombol ini hanya untuk admin!", True)

    # Hapus status pause jika ada
    if chat_id in paused:
        del paused[chat_id]

    # Cek apakah ada antrian
    if chat_id not in playlist or len(playlist[chat_id]) <= 1:
        return await cq.answer("Tidak ada antrian berikutnya!", True)

    # Hapus lagu yang sedang dimainkan
    current = playlist[chat_id].pop(0)
    next_song = playlist[chat_id][0]

    # Mainkan lagu berikutnya
    await c.assistant.play(chat_id, MediaStream(next_song['lagu']))

    # Kirim notifikasi ke chat
    if next_song['thumb']:
        await c.send_photo(
            chat_id,
            next_song['thumb'],
            caption=f"<i><b>Memutar antrian berikutnya:</b>\n\n{next_song['judul']}</i>",
            reply_markup=InlineKeyboardMarkup(BTN.PLAY())
        )
    else:
        await c.send_message(
            chat_id,
            f"<i><b>Memutar antrian berikutnya:</b>\n\n{next_song['judul']}</i>",
            reply_markup=InlineKeyboardMarkup(BTN.PLAY())
        )

    # Beri respon ke callback
    await cq.answer("Memutar lagu berikutnya!", True)

    # (❗ opsional) Hapus file lagu sebelumnya setelah skip
    thumb = current.get("thumb")
    bersihkan(current["lagu"], thumb)


@USU.CALLBACK("stop")
async def sto(c, cq):
    if cq.from_user:
        jepret = f"{cq.from_user.first_name} {cq.from_user.last_name or ''}"
    else:
        jepret = f"{cq.message.sender_chat.title}"
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    a_calls = await c.assistant.calls
    if_chat = a_calls.get(chat_id)
    admin = await list_admins(c, cq.message.chat.id)
    if user_id not in admin and user_id not in DEVS:
        return await cq.answer(f"Tombol ini untuk admin!", True)
    if chat_id in paused:
        del paused[chat_id]
    if chat_id not in playlist:
        return await cq.answer(f"Tidak ada streaming yang aktif!", True)
    if chat_id in playlist:
        del playlist[chat_id]
    await c.assistant.leave_call(chat_id)
    await bot.send_message(chat_id, f"<i><b>Streaming end by {jepret}</b></i>")   
    return await cq.answer(f"Streaming end!", True)

@USU.CALLBACK("tutup")
async def _(c, cq):
    user_id = cq.from_user.id
    admin = await list_admins(c, cq.message.chat.id)
    if user_id not in admin and user_id not in DEVS:
        return await cq.answer(f"Tombol ini untuk admin!", True)
    return await cq.message.delete()

@USU.CALLBACK("ps")
async def pause_client(c, cq):
    global orang, playlist
    data = cq.data.split()
    user_id = int(data[1])
    chat_id = int(data[2])
    if user_id in orang:
        usernya = orang[user_id]
        a_calls = await usernya.call_py.calls
        if_chat = a_calls.get(chat_id)
        admin = await list_admins(usernya, chat_id)
        if cq.from_user.id not in admin and cq.from_user.id not in DEVS:
            return await cq.answer(f"Tombol ini untuk admin!", True)

        if chat_id not in playlist.get(user_id, {}):
            return await cq.answer(f"Tidak ada streaming yang aktif!", True)
        if user_id not in paused:
            paused[user_id] = {}
        if user_id in paused and chat_id in paused[user_id]:
            return await cq.answer(f"Streaming sudah dalam keadaan pause!", True)
        await usernya.call_py.pause_stream(chat_id)
        if user_id in playtask and chat_id in playtask[user_id]:
            task = playtask[user_id][chat_id]
            task.cancel()
        await cq.answer(f"Streaming di-pause!", True)
        paused[user_id][chat_id] = True
    else:
        return await cq.answer(f"Tidak ada streaming yang aktif!", True)


@USU.CALLBACK("rsm")
async def resume_client(c, cq):
    global orang, playlist
    data = cq.data.split()
    user_id = int(data[1])
    chat_id = int(data[2])
    if user_id in orang:
        usernya = orang[user_id]
        a_calls = await usernya.call_py.calls
        if_chat = a_calls.get(chat_id)
        admin = await list_admins(usernya, chat_id)
        if cq.from_user.id not in admin and cq.from_user.id not in DEVS:
            return await cq.answer(f"Tombol ini untuk admin!", True)

        if user_id not in playlist and chat_id not in playlist[user_id]:
            return await cq.answer(f"Tidak ada streaming yang aktif!", True)
        if user_id in paused and chat_id not in paused[user_id]:
            return await cq.answer(f"Streaming sedang tidak di-pause!", True)

        await usernya.call_py.resume_stream(chat_id)
        await cq.answer(f"Streaming di-resume!", True)
        del paused[user_id][chat_id]
        if user_id not in playtask:
            playtask[user_id] = {}
        playtask[user_id][chat_id] = loop.create_task(
            next_song(usernya, chat_id, playlist[user_id][chat_id][0]['duration'])
        )
    else:
        return await cq.answer(f"Tidak ada streaming yang aktif!", True)


@USU.CALLBACK("skp")
async def skip_client(c, cq):
    global orang, playlist
    data = cq.data.split()
    user_id = int(data[1])
    chat_id = int(data[2])

    if user_id not in orang:
        return await cq.answer("User tidak aktif!", True)

    usernya = orang[user_id]
    sks = await EMO.SUKSES(usernya)
    a_calls = await usernya.call_py.calls
    if_chat = a_calls.get(chat_id)
    admin = await list_admins(usernya, chat_id)

    # Hanya admin/DEVS yang bisa tekan skip
    if cq.from_user.id not in admin and cq.from_user.id not in DEVS:
        return await cq.answer("Tombol ini hanya untuk admin!", True)

    # Hapus status pause jika ada
    if user_id in paused and chat_id in paused[user_id]:
        del paused[user_id][chat_id]

    # Cek jika ada antrian
    if user_id in playlist and chat_id in playlist[user_id] and len(playlist[user_id][chat_id]) > 1:
        try:
            next_track = playlist[user_id][chat_id][1]
            current_track = playlist[user_id][chat_id][0]

            # Batalkan task lama jika masih berjalan
            if user_id in playtask and chat_id in playtask[user_id]:
                task = playtask[user_id][chat_id]
                if not task.done():
                    task.cancel()

            # Mainkan lagu berikut
            await usernya.call_py.play(chat_id, MediaStream(next_track['lagu']))

            # Bersihkan lagu lama, bukan lagu baru
            bersihkan(current_track['lagu'], current_track['thumb'])

            # Hapus lagu lama dari antrian
            playlist[user_id][chat_id].pop(0)

            # Jadwalkan lagu berikut
            playtask[user_id][chat_id] = loop.create_task(
                next_song(usernya, chat_id, next_track['duration'])
            )

            hasil_text = f"<b>{sks}Memutar antrian!</b>"
            hasil = next_track['judul']

            try:
                x = await usernya.get_inline_bot_results(
                    bot.me.username,
                    f"play|{user_id}|{chat_id}|{hasil_text}"
                )
                await usernya.send_inline_bot_result(
                    chat_id,
                    x.query_id,
                    x.results[0].id,
                )
            except (ChatSendMediaForbidden, ChatSendInlineForbidden):
                await usernya.send_message(chat_id, f"<i>{hasil_text}\n\n{hasil}</i>")
            except Exception as e:
                await usernya.send_message(chat_id, f"⚠️ {str(e)}")

            await cq.answer("Memutar antrian berikutnya!", True)

        except Exception as e:
            return await cq.answer(f"⚠️ Error: {str(e)}", True)
    else:
        return await cq.answer("Tidak ada antrian streaming!", True)



@USU.CALLBACK("stp")
async def stop_client(c, cq):
    global orang, playlist
    data = cq.data.split()
    user_id = int(data[1])
    chat_id = int(data[2])
    if user_id in orang:
        usernya = orang[user_id]
        a_calls = await usernya.call_py.calls
        if_chat = a_calls.get(chat_id)
        admin = await list_admins(usernya, chat_id)
        if cq.from_user.id not in admin and cq.from_user.id not in DEVS:
            return await cq.answer(f"Tombol ini untuk admin!", True)
        if user_id in paused and chat_id in paused[user_id]:
            del paused[user_id][chat_id]
        if chat_id not in playlist.get(user_id, {}):
            return await cq.answer(f"Tidak ada streaming yang aktif!", True)
        if user_id in playlist and chat_id in playlist[user_id]:
            del playlist[user_id][chat_id]
        if user_id in orang:
            del orang[user_id]
        if user_id in playtask and chat_id in playtask[user_id]:
            task = playtask[user_id][chat_id]
            task.cancel()
            del playtask[user_id][chat_id]
        await usernya.call_py.leave_call(chat_id)  
        return await cq.answer(f"Streaming end!", True)


@USU.CALLBACK("ttp")
async def tutup_client(c, cq):
    global orang, playlist
    data = cq.data.split()
    user_id = int(data[1])
    chat_id = int(data[2])
    if user_id in orang:
        usernya = orang[user_id]
        admin = await list_admins(usernya, chat_id)
        if cq.from_user.id not in admin and cq.from_user.id not in DEVS:
            return await cq.answer(f"Tombol ini untuk admin!", True)
        return await cq.answer(f"Tombol ini cuman pajangan!", True)