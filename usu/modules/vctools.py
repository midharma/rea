import asyncio
from random import randint

from pytgcalls.types import *
from pytgcalls.exceptions import *
from youtubesearchpython import VideosSearch

from pyrogram import *
from pyrogram.types import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall, EditGroupCallTitle, GetGroupCall
from pyrogram.raw.types import InputPeerChannel, InputPeerChat, GroupCallParticipant
from pyrogram.raw.base import InputGroupCall
from pyrogram.errors import FloodWait, MessageNotModified

from usu import *

from pyrogram.errors import ChatSendInlineForbidden, ChatForbidden, QueryIdInvalid, Forbidden




JOINVC = """Command for <b>Join-VC</b>

<b>Join-VC</b>
 <i>bergabung ke obrolan suara</i>
    <code>{0}joinvc</code>"""

LEAVEVC = """Command for <b>Leave-VC</b>

<b>Leave-VC</b>
 <i>meninggalkan obrolan suara</i>
    <code>{0}leavevc</code>"""

SETVC = """Command for <b>Set-VC</b>

<b>Set-VC</b>
 <i>mengganti judul obrolan suara</i>
    <code>{0}setvc</code> [judul]"""

LISTVC = """Command for <b>List-VC</b>

<b>List-VC</b>
 <i>cek peserta obrolan suara</i>
    <code>{0}listvc</code>"""

STARTVC = """Command for <b>Start-VC</b>

<b>Start-VC</b>
 <i>memulai obrolan suara</i>
    <code>{0}startvc</code>"""

STOPVC = """Command for <b>Stop-VC</b>

<b>Stop-VC</b>
 <i>mengakhiri obrolan suara</i>
    <code>{0}stopvc</code>"""


PLAY = """Command for <b>Play-Music/Video</b>

<b>Play-Music/Video</b>
 <i>Play music di obrolan suara</i> 
    <code>{0}play</code> [judul]
 <i>Play video di obrolan suara</i> 
    <code>{0}vplay</code> [judul]"""

PAUSEMUSIC = """Command for <b>Pause-Music</b>

<b>Pause-Music</b>
 <i>Pause music/video di obrolan suara</i>
    <code>{0}pause</code>"""

RESUMEMUSIC = """Command for <b>Resume-Music</b>

<b>Resume-Music</b>
 <i>Resume music/video di obrolan suara</i>
    <code>{0}resume</code>"""

SKIPMUSIC = """Command for <b>Skip-Music</b>

<b>Skip-Music</b>
 <i>Skip music/video di obrolan suara</i>
    <code>{0}skip</code>"""

PLAYLISTMUSIC = """Command for <b>Playlist-Music</b>

<b>Playlist-Music</b>
  <i>Playlist music/video di obrolan suara</i>
    <code>{0}playlist</code>"""

ENDMUSIC = """Command for <b>End-Music</b>

<b>End-Music</b>
  <i>End music/video di obrolan suara</i>
    <code>{0}end</code>"""


__UTAMA__ = "VC-Tools"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Joinvc", "Leavevc", "Startvc", "Stopvc", "Setvc", "Listvc", "Play", "End", "Resume", "Pause", "Skip", "Playlist"

__HASIL__ = JOINVC, LEAVEVC, STARTVC, STOPVC, SETVC, LISTVC, PLAY, ENDMUSIC, RESUMEMUSIC, PAUSEMUSIC, SKIPMUSIC, PLAYLISTMUSIC


trigger_id = {}


async def get_group_call(client, message):
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.reply(f"<i><b>Voice chats not active!</b></i>")
    return False

@USU.UBOT("jvc")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    usu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    if not chat_id:
        return await usu.edit(f"<i><b>{ggl}Invalid!</b></i>")

    for x_ in ubot._ubot.values():
        try:
            a_calls = await x_.call_py.calls
            if_chat = a_calls.get(chat_id)
            if if_chat:
                continue
            await x_.call_py.play(chat_id)
            await x_.call_py.mute_stream(chat_id)
        except NoActiveGroupCall as e:
            pass
        except Exception as e:
            pass
    await usu.delete()
    return await message.reply(f"""<b><i>{sks}All clients joined in group calls!</i></b>""")


@USU.UBOT("lvc")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    usu = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    if not chat_id:
        return await usu.edit(f"<i><b>{ggl}Invalid!</b></i>")

    for x_ in ubot._ubot.values():
        try:
            a_calls = await x_.call_py.calls
            if_chat = a_calls.get(chat_id)
            if not if_chat:
                continue
            await x_.call_py.leave_call(chat_id)
        except GroupCallNotFound:
            pass
        except Exception as e:
            pass
    await usu.delete()
    return await message.reply(f"""<b><i>{sks}All clients leave in group calls!</i></b>""")


@USU.UBOT("startvc")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    flags = " ".join(message.command[1:])
    _msg = f"""<b><i>{prs}Processing...</i></b>"""

    msg = await message.reply(_msg)
    vctitle = get_arg(message)
    chat_id = message.chat.id

    args = f"""<b><i>{sks}Successfully started voice chat!</i></b>"""

    try:
        if vctitle:
            args += f"\n<i><b>{broad}Title:</b> {vctitle}</i>"

        await client.invoke(
            CreateGroupCall(
                peer=(await client.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
                title=vctitle if vctitle else None,
            )
        )
        await msg.edit(args)
    except Exception as e:
        await msg.edit(f"INFO: {e}")


@USU.UBOT("stopvc")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"""<b><i>{prs}Processing...</i></b>"""

    msg = await message.reply(_msg)
    group_call = await get_group_call(client, message)

    if not group_call:
        return await msg.edit(f"""<i><b>{ggl}No active voice chat!</b></i>""")

    await client.invoke(DiscardGroupCall(call=group_call))
    await msg.edit(
        f"""<b><i>{sks}Stop voice chat!</i></b>"""
    )

@USU.INLINE("voicechat")
async def inline_voicechat(client, inline_query):
    args = inline_query.query.split(None, 3)
    chat_id = int(args[1])
    m = int(args[2])
    text = args[3]
    try:
        results = [
            InlineQueryResultArticle(
                title="Voice Chat",
                input_message_content=InputTextMessageContent(text),
                reply_markup=InlineKeyboardMarkup(
                     BTN.VOICE(m, chat_id)
                ),
            )
        ]
        await inline_query.answer(results=results)
    except (BotResponseTimeout, QueryIdInvalid):
        pass
    except Exception as e:
        logger.exception(e)


@USU.CALLBACK("joinvc|leavevc")
async def cancel_broadcast(client, callback_query):
    args = callback_query.data.split(maxsplit=2)
    user_id = int(args[1])
    chat_id = int(args[2])
    a_calls = await ubot._ubot[user_id].call_py.calls
    if_chat = a_calls.get(chat_id)
    cb = callback_query.from_user
    if cb.id not in trigger_id and cb.id not in DEVS:
        return await callback_query.answer(f"❌ Tombol ini bukan untuk anda!", True) 
    if args[0] == "joinvc":
        if if_chat:
            return await callback_query.answer(f"❌ Anda sudah berada di voice chat!", True)
        await ubot._ubot[user_id].call_py.play(chat_id)
        await ubot._ubot[user_id].call_py.mute_stream(chat_id)
        return await callback_query.answer(f"✅ Berhasil memasuki voice chat!", True)
    else:
        if not if_chat:
            return await callback_query.answer(f"❌ Anda belum berada di voice chat!", True)
        await ubot._ubot[user_id].call_py.leave_call(chat_id)
        return await callback_query.answer(f"✅ Berhasil keluar voice chat!", True)



async def joinvc_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    mg = client.me if message.from_user else message.sender_chat
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if not chat_id:
        return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")
    if if_chat:
        return await message.reply(f"<i><b>{ggl}Already on voice chat</b></i>")
    msg_ = f"""<b><i>{sks}Successfully join voice chat!</i></b>"""
    try:
        await client.call_py.play(chat_id)
        await client.call_py.mute_stream(chat_id)
        x = await client.get_inline_bot_results(bot.me.username, f"voicechat {chat_id} {client.me.id} {msg_}")
        if not x.results:
            return await message.reply(msg_)
        msg = await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        trigger_id[mg.id] = client.me.id
    except (ChatSendInlineForbidden, BotResponseTimeout, QueryIdInvalid, Forbidden):
        return await message.reply(msg_)
    except (ChatForbidden, Forbidden):
        pass
    except NoActiveGroupCall:
        return await message.reply(f"""<b><i>{ggl}No voice chat!</i></b>""")
    except Exception as e:
        return await message.reply(f"<i><b>{ggl}Error:</b> {e}</i>")


async def joinvc_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if not chat_id:
        return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")
    if if_chat:
        return await message.reply(f"<i><b>{ggl}Already on voice chat</b></i>")
    try:
        await client.call_py.play(chat_id)
        await client.call_py.mute_stream(chat_id)
        return await message.reply(f"""<b><i>{sks}Successfully join voice chat!</i></b>""")
    except NoActiveGroupCall:
        return await message.reply(f"""<b><i>{ggl}No voice chat!</i></b>""")
    except Exception as e:
        return await message.reply(f"<i><b>{ggl}Error:</b> {e}</i>")


@USU.UBOT("joinvc")
@ubot.on_message(filters.user(DEVS) & filters.command("cjoinvc", ""))
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await joinvc_inline(client, message)
    else:
        await joinvc_ori(client, message)


async def leavevc_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    mg = client.me if message.from_user else message.sender_chat
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if not chat_id:
        return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")
    if not if_chat:
        return await message.reply(f"""<b><i>{ggl}Not in voice chat!</i></b>""")
    msg_ = f"""<b><i>{sks}Successfully leave voice chat!</i></b>"""
    try:
        await client.call_py.leave_call(chat_id)
        x = await client.get_inline_bot_results(bot.me.username, f"voicechat {chat_id} {client.me.id} {msg_}")
        if not x.results:
            return await message.reply(msg_)
        msg = await message.reply_inline_bot_result(x.query_id, x.results[0].id)
        trigger_id[mg.id] = client.me.id
    except (ChatSendInlineForbidden, BotResponseTimeout, QueryIdInvalid):
        return await message.reply(msg_)
    except (ChatForbidden, Forbidden):
        pass
    except Exception as e:
        return await message.reply(f"<i><b>{ggl}Error:</b> {e}</i>")


async def leavevc_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) > 1:
        input_identifier = message.command[1]
    else:
        input_identifier = message.chat.id

    chat_id = await extract_id(message, input_identifier)
    a_calls = await client.call_py.calls
    if_chat = a_calls.get(chat_id)
    if not chat_id:
        return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")
    if not if_chat:
        return await message.reply(f"""<b><i>{ggl}Not in voice chat!</i></b>""")
    try:
        await client.call_py.leave_call(chat_id)
        return await message.reply(f"""<b><i>{sks}Successfully leave voice chat!</i></b>""")
    except Exception as e:
        return await message.reply(f"<i><b>{ggl}Error:</b> {e}</i>")

@USU.UBOT("leavevc")
@ubot.on_message(filters.user(DEVS) & filters.command("cleavevc", ""))
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await leavevc_inline(client, message)
    else:
        await leavevc_ori(client, message)

@USU.UBOT("setvc")
async def set_vc(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"""<b><i>{prs}Processing...</i></b>"""

    msg = await message.reply(_msg)
    new_title = get_arg(message)
    if not new_title:
        return await msg.edit(f"""<b><i>{ggl}Invalid!</i></b>""")

    try:
        group_call = await get_group_call(client, message)
        if group_call:
            await client.invoke(EditGroupCallTitle(call=group_call, title=new_title))
            await msg.edit(f"""<b><i>{sks}Successfully changed voice chat title!</i></b>""")
    except Exception as e:
        await msg.edit(f"<i><b>{ggl}Error:</b> {str(e)}</i>")


@USU.UBOT("listvc")
async def tampilkan_peserta_obrolan_suara(c, m):
    sks = await EMO.SUKSES(c)
    ggl = await EMO.GAGAL(c)
    prs = await EMO.PROSES(c)
    broad = await EMO.BROADCAST(c)
    ptr = await EMO.PUTARAN(c)
    usu = await m.reply(f"<b><i>{prs}Processing...</i></b>")
    if len(m.command) > 1:
        input_identifier = m.command[1]
    else:
        input_identifier = m.chat.id
    chat_id = await extract_id(m, input_identifier)
    try:
        chat = await c.get_chat(chat_id)
        title = chat.title if chat.title else f"{chat_id}"
        group_call = await get_group_call(c, m)
        if not group_call:
            return await usu.edit(
                f"<b><i>{ggl}Not voice chats</i></b>"
            )
        try:
            participants = await c.call_py.get_participants(chat_id)
            if not participants:
                return await usu.edit(f"<b><i>{ggl}Empty!</i></b>")
            hasil = []
            for a, participant in enumerate(participants):
                user_id = participant.user_id
                try:
                    user = await c.get_users(user_id)
                    mention = user.mention
                    status = "Unmuted" if participant.muted else "Muted"
                    volume = participant.volume
                    hasil.append(f"<b>{a+1}.Name:</b> {mention} <b>| Mic:</b> {status} <b>| Volume:</b> {volume}%")
                except Exception as e:
                    user = await c.get_chat(user_id)
                    mention = user.title
                    status = "Unmuted" if participant.muted else "Muted"
                    volume = participant.volume
                    hasil.append(f"<b>{a+1}.Name:</b> {mention} <b>| Mic:</b> {status} <b>| Volume:</b> {volume}%")

            total_participants = len(participants)
            mentions_text = "\n".join(hasil)
            text = f"""<b>{broad}Voice Chat Participant!</b>
<b>{ptr}Chat Title:</b> {title}
<b>{sks}Total Participant:</b> {total_participants}

{mentions_text}
"""
        except Exception as e:
            return await usu.edit(e)
    except Exception as e:
        return await usu.edit(e)

    await usu.delete()
    return await m.reply(f"<i>{text}</i>")


#========



@USU.BOT("startvc")
@USU.ADMIN
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    flags = " ".join(message.command[1:])
    _msg = f"""<b><i>Processing...</i></b>"""

    msg = await message.reply(_msg)
    vctitle = get_arg(message)
    chat_id = message.chat.id

    args = f"""<b><i>{sks}Successfully started voice chat!</i></b>"""

    try:
        if vctitle:
            args += f"\n<i><b>{broad}Title:</b> {vctitle}</i>"

        await client.usu.invoke(
            CreateGroupCall(
                peer=(await client.usu.resolve_peer(chat_id)),
                random_id=randint(10000, 999999999),
                title=vctitle if vctitle else None,
            )
        )
        await msg.edit(args)
    except Exception as e:
        return await msg.edit(f"<i><b>{ggl}Silahkan beri akses admin ke Assistant!</b></i>")



@USU.BOT("stopvc")
@USU.ADMIN
@USU.GC
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"""<b><i>{prs}Processing...</i></b>"""

    msg = await message.reply(_msg)
    group_call = await get_group_call(client.usu, message)

    if not group_call:
        return await msg.edit(f"""<i><b>{ggl}No active voice chat!</b></i>""")
    try:
        await client.usu.invoke(DiscardGroupCall(call=group_call))
        await msg.edit(
            f"""<b><i>{sks}Stop voice chat!</i></b>"""
        )
    except Exception as e:
        return await msg.edit(f"<i><b>{ggl}Silahkan beri akses admin ke Assistant!</b></i>")



@USU.BOT("setvc")
@USU.ADMIN
@USU.GC
async def set_vc(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"""<b><i>{prs}Processing...</i></b>"""

    msg = await message.reply(_msg)
    new_title = get_arg(message)
    if not new_title:
        return await msg.edit(f"""<b><i>{ggl}Invalid!</i></b>""")

    try:
        group_call = await get_group_call(client.usu, message)
        if group_call:
            await client.usu.invoke(EditGroupCallTitle(call=group_call, title=new_title))
            await msg.edit(f"""<b><i>{sks}Successfully changed voice chat title!</i></b>""")
    except Exception as e:
        return await msg.edit(f"<i><b>{ggl}Silahkan beri akses admin ke Assistant!</b></i>")


@USU.BOT("listvc")
@USU.ADMIN
@USU.GC
async def tampilkan_peserta_obrolan_suara(c, m):
    sks = await EMO.SUKSES(c)
    ggl = await EMO.GAGAL(c)
    prs = await EMO.PROSES(c)
    broad = await EMO.BROADCAST(c)
    ptr = await EMO.PUTARAN(c)
    usu = await m.reply(f"<b><i>{prs}Processing...</i></b>")
    if len(m.command) > 1:
        input_identifier = m.command[1]
    else:
        input_identifier = m.chat.id
    chat_id = await extract_id(m, input_identifier)
    try:
        chat = await c.get_chat(chat_id)
        title = chat.title if chat.title else f"{chat_id}"
        group_call = await get_group_call(c, m)
        if not group_call:
            return await usu.edit(
                f"<b><i>{ggl}Not voice chats</i></b>"
            )
        try:
            participants = await c.assistant.get_participants(chat_id)
            if not participants:
                return await usu.edit(f"<b><i>{ggl}Empty!</i></b>")
            hasil = []
            for a, participant in enumerate(participants):
                user_id = participant.user_id
                try:
                    user = await c.get_users(user_id)
                    mention = user.mention
                    status = "Unmuted" if participant.muted else "Muted"
                    volume = participant.volume
                    hasil.append(f"<b>{a+1}.Name:</b> {mention} <b>| Mic:</b> {status} <b>| Volume:</b> {volume}%")
                except Exception as e:
                    user = await c.get_chat(user_id)
                    mention = user.title
                    status = "Unmuted" if participant.muted else "Muted"
                    volume = participant.volume
                    hasil.append(f"<b>{a+1}.Name:</b> [{mention}]({user.invite_link}) <b>| Mic:</b> {status} <b>| Volume:</b> {volume}%")

            total_participants = len(participants)
            mentions_text = "\n".join(hasil)
            text = f"""<b>{broad}Voice Chat Participant!</b>
<b>{ptr}Chat Title:</b> {title}
<b>{sks}Total Participant:</b> {total_participants}

{mentions_text}
"""
        except Exception as e:
            return await usu.edit(e)
    except Exception as e:
        return await usu.edit(e)

    await usu.delete()
    return await m.reply(f"<i>{text}</i>", disable_web_page_preview=True)

@USU.BOT("activevc")
@USU.SUDO
async def tampilkan_peserta_obrolan_suara(c, m):
    if not bot.assistant:
        return
    group = await db.get_list_from_vars(bot.me.id, "group")
    channel = await db.get_list_from_vars(bot.me.id, "channel")
    chat = []
    chat.extend(group)
    chat.extend(channel)
    hasil = []
    asoy = []
    a_calls = await c.assistant.calls
    for chat_id in chat:
        if_chat = a_calls.get(chat_id)
        if if_chat:
            asoy.append(chat_id)
    if asoy:
        for angka, gbt in enumerate(asoy, start=1): 
            try:
                peserta = await c.assistant.get_participants(gbt)
                anu = await c.get_chat(gbt)
                asu = f"[{anu.title}]({anu.invite_link})" if anu.invite_link else f"[{anu.title}](https://t.me/{anu.username})" if anu.username else anu.id
                hasil.append(f"<b>{angka}.Name:</b> {asu} <b>| Total Peserta:</b> {len(peserta)}")
            except Exception as e:
                logger.error(e)
    if hasil:
        teks = f"<b>Music Aktif:\n</b>" + "\n".join(hasil)
    else:
        teks = f"<b>Tidak ada chat yang tersedia!</b>"
    return await m.reply(f"<i>{teks}</i>", disable_web_page_preview=True)
        
           
            
    