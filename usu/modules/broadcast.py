import asyncio
import random

import os
import json
import asyncio
import psutil

from pyrogram.raw import *
from pyrogram import Client

from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.errors import ChatSendInlineForbidden, ChatForbidden, BotResponseTimeout, QueryIdInvalid, Forbidden


from pyrogram.errors import (
    FloodWait,
    ChannelPrivate,
    SlowmodeWait,
    ChatWriteForbidden,
    Forbidden,
    UserBannedInChannel,
    PeerIdInvalid
)
from pyrogram.types import (
    InputMediaPhoto,
    InputMediaVideo
)

from usu import *
from usu.config import BLACKLIST_CHAT


BLACKLIST = """Command for <b>Blacklist</b>

<b>Broadcast blacklist</b>
 <i>memasukan group ke daftar blacklist</i>
    <code>{0}addbl</code>
 <i>menghapus group dari daftar blacklist</i>
    <code>{0}unbl</code>
 <i>menghapus semua daftar blacklist group</i>
    <code>{0}clearbl</code>
 <i>memeriksa daftar blacklist group</i>
    <code>{0}listbl</code>

<b>Note:</b>
<i>pesan broadcast anda tidak akan masuk ke group yang di blacklist</i>"""


SIARAN = """Command for <b>Broadcast</b>

<b>Type</b>
 <code>'group'</code> , kirim pesan ke semua group
 <code>'users'</code> , kirim pesan ke semua pengguna
 <code>'channel'</code> , kirim pesan ke semua channel
 <code>'all'</code> , kirim pesan ke chat
 <code>'db'</code> , kirim pesan ke database

 <i>mengirim pesan/media ke semua [type]</i>
   <code>{0}bc</code> [type] [text/media]

 <i>mengirim pesan/media ke semua group</i>
   <code>{0}gcast</code> [text/media]

 <i>mengirim pesan/media ke semua users</i>
   <code>{0}ucast</code> [text/media]

 <i>cancel broadcast</i>
   <code>{0}cancelbc</code>

 <i>mengirim pesan secara fordward</i>
   <code>{0}bcfd</code>

 <i>mengirim pesan melalui username</i>
   <code>{0}send</code> [username]

<b>Query AutoBroadcast</b>
 <code>'on/off'</code> , mengaktifkan/menonaktifkan
 <code>'text'</code> , mengatur pesan [text]
 <code>'delay'</code> , mengatur waktu pesan [angka]
 <code>'limit'</code> , mengaktifkan limit [on/off]
 <code>'remove'</code> , mereset pesan [angka/all]
 <code>'list'</code> , melihat daftar pesan text

 <i>mengirim pesan semua group secara otomatis</i>
   <code>{0}autobc</code> [query] [value]"""

BCDB = """Command for <b>Broadcast-Database</b>

<b>Type</b>
 <code>'db'</code> , kirim pesan ke database

 <i>mengirim pesan/media ke semua database</i>
   <code>{0}bc</code> [db] [text/media]

 <i>mengirim pesan/media forward ke semua database</i>
   <code>{0}bcfd</code> [db] [text/media]

 <i>cancel broadcast</i>
   <code>{0}cancelbc</code>

<b>Broadcast database</b>
 <i>memasukan group ke daftar database broadcast</i>
    <code>{0}addbcdb</code>
 <i>menghapus group dari daftar database broadcast</i>
    <code>{0}unbcdb</code>
 <i>menghapus semua daftar database broadcast</i>
    <code>{0}clearbcdb</code>
 <i>memeriksa daftar database broadcast</i>
    <code>{0}listbcdb</code>


<b>Note:</b>
<i>pesan broadcast anda akan masuk ke dalam group yang di database</i>"""

SPAMG = """Command for <b>SpamG</b>

<b>SpamG</b>
 <i>melakukan spam ke seluruh group</i>
    <code>{0}spamg</code> [text/reply] [jumlah]
 <i>cancel spam gcast</i>
    <code>{0}cancelspamg</code>"""


__UTAMA__ = "Broadcasts"
__TEXT__ = f"Menu Bantuan {__UTAMA__}!"
__BUTTON__ = "Broadcast", "Blacklist", "Broadcast-DB", "SpamG"
__HASIL__ = SIARAN, BLACKLIST, BCDB, SPAMG



async def limit_cmd(client, message):
    prs = await EMO.PROSES(client)
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    _msg = f"<b><i>{prs}Processing...</i></b>"

    msg = await message.reply(_msg)
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    await msg.delete()
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1)
    await status.copy(message.chat.id, reply_to_message_id=message.id)
    return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))


broadcasts = []


async def gcast_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    send = get_message(message)
    if not send:
        await eor(message, f"<b><i>{ggl}Reply/Text</i></b>")
        return
    broadcasts.append(client.me.id)
    msg_ = f"""<b><i>{prs}{prs_gcst}</i></b>"""
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"broadcast|{client.me.id}|{msg_}")
        if not x.results:
            msg = await message.reply(msg_)
        else:
            msg = await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except (ChatSendInlineForbidden, BotResponseTimeout, QueryIdInvalid):
        msg = await message.reply(msg_)
    except (ChatForbidden, Forbidden):
        pass
    chats = await get_data_id(client, "group")
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")
    done = 0
    failed = 0
    hasil = []
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                if message.reply_to_message:
                    await send.copy(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts:
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await message.reply(f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group</i>""")
    else:
        broadcasts.remove(client.me.id)
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await message.reply(f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass


@USU.INLINE("broadcast")
async def inline_broadcast(client, inline_query):
    args = inline_query.query.split("|", 2)
    x = int(args[1])
    text = args[2]
    try:
        results = [
            InlineQueryResultArticle(
                title="📢 Broadcast",
                input_message_content=InputTextMessageContent(text),
                reply_markup=InlineKeyboardMarkup(
                    BTN.BC(x)
                ),
            )
        ]
        await inline_query.answer(results=results)
    except (BotResponseTimeout, QueryIdInvalid):
        pass
    except Exception as e:
        logger.exception(e)



async def gcast_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    broadcasts.append(client.me.id)
    send = get_message(message)
    if not send:
        await eor(message, f"<b><i>{ggl}Reply/Text</i></b>")
        broadcasts.remove(client.me.id)
        return
    done = 0
    failed = 0
    hasil = []
    msg = await message.reply(f"""<b><i>{prs}{prs_gcst}</i></b>""")
    chats = await get_data_id(client, "group")
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                if message.reply_to_message:
                    await send.copy(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts:
        await msg.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group</i>""")
    else:
        broadcasts.remove(client.me.id)
        await msg.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass


@USU.UBOT("gcast")
@ubot.on_message(filters.command("cgcast", "") & filters.user(DEVS))
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await gcast_inline(client, message)
    else:
        await gcast_ori(client, message)


@USU.CALLBACK("^cancel_broadcast")
async def cancel_broadcast(client, callback_query):
    args = callback_query.data.split(maxsplit=1)
    user_id = int(args[1])
    if callback_query.from_user.id == user_id:    
        if user_id in broadcasts:
            broadcasts.remove(user_id)
            await callback_query.answer("✅ Broadcast dihentikan!", show_alert=True)
        else:
            await callback_query.answer("⚠️ Tidak ada broadcast yang berjalan.", show_alert=True)
    else:
        return await callback_query.answer("⚠️ Anda tidak dapat menghentikan broadcast ini.", show_alert=True)



async def ucast_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    send = get_message(message)
    if not send:
        await eor(message, f"<b><i>{ggl}Reply/Text</i></b>")
        return
    broadcasts.append(client.me.id)
    msg_ = f"""<b><i>{prs}{prs_gcst}</i></b>"""
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"broadcast|{client.me.id}|{msg_}")
        if not x.results:
            msg = await message.reply(msg_)
        else:
            msg = await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except (ChatSendInlineForbidden, BotResponseTimeout, QueryIdInvalid):
        msg = await message.reply(msg_)
    except (ChatForbidden, Forbidden):
        pass
    chats = await get_data_id(client, "users")
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")
    done = 0
    failed = 0
    hasil = []
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                if message.reply_to_message:
                    await send.copy(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts:
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> users</i>""")
    else:
        broadcasts.remove(client.me.id)
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> users</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass

async def ucast_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    send = get_message(message)
    if not send:
        await eor(message, f"<b><i>{ggl}Reply/Text</i></b>")
        return
    broadcasts.append(client.me.id)
    done = 0
    failed = 0
    hasil = []
    msg = await message.reply(f"""<b><i>{prs}{prs_gcst}</i></b>""")
    chats = await get_data_id(client, "users")
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            if message.reply_to_message:
                await send.copy(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                if message.reply_to_message:
                    await send.copy(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts:
        await msg.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> users</i>""")
    else:
        broadcasts.remove(client.me.id)
        await msg.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> users</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass

@USU.UBOT("ucast")
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await ucast_inline(client, message)
    else:
        await ucast_ori(client, message)


async def bc_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    broadcasts.append(client.me.id)
    command, text = extract_type_and_msg(message)

    if command not in ["group", "users", "all", "db", "channel"] or not text:
        return await message.reply(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[group/channel/users/all] [text/reply]</b></i>")
    broadcasts.append(client.me.id)
    msg_ = f"""<b><i>{prs}{prs_gcst}</i></b>"""
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"broadcast|{client.me.id}|{msg_}")
        if not x.results:
            msg = await message.reply(msg_)
        else:
            msg = await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except (ChatSendInlineForbidden, BotResponseTimeout, QueryIdInvalid):
        msg = await message.reply(msg_)
    except (ChatForbidden, Forbidden):
        pass
    chats = await get_data_id(client, command)
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    hasil = []
    for chat_id in chats:
        if chat_id in await db.get_list_from_vars(client.me.id, "bcdb"):
            if command == "db":
                try:
                    if client.me.id not in broadcasts:
                        break
                    await client.send_chat_action(chat_id, ChatAction.TYPING)
                    await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                    done += 1
                except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await client.send_chat_action(chat_id, ChatAction.TYPING)
                    await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                    done += 1
                    if client.me.id not in broadcasts:
                        break
                except Exception:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts:
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    else:
        broadcasts.remove(client.me.id)
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass




async def bc_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    _msg = await eor(message, f"""<b><i>{prs}{prs_gcst}</i></b>""")

    command, text = extract_type_and_msg(message)

    if command not in ["group", "users", "all", "db", "channel"] or not text:
        return await _msg.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[group/channel/users/all] [text/reply]</b></i>")
    broadcasts.append(client.me.id)
    chats = await get_data_id(client, command)
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    hasil = []
    for chat_id in chats:
        if chat_id in await db.get_list_from_vars(client.me.id, "bcdb"):
            if command == "db":
                try:
                    if client.me.id not in broadcasts:
                        break
                    await client.send_chat_action(chat_id, ChatAction.TYPING)
                    await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                    done += 1
                except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await client.send_chat_action(chat_id, ChatAction.TYPING)
                    await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                    done += 1
                    if client.me.id not in broadcasts:
                        break
                except Exception:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                await (text.copy(chat_id) if message.reply_to_message else client.send_message(chat_id, text))
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts:
        await _msg.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    else:
        broadcasts.remove(client.me.id)
        await _msg.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass



@USU.UBOT("bc")
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await bc_inline(client, message)
    else:
        await bc_ori(client, message)


@USU.UBOT("cancelbc")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if client.me.id not in broadcasts:
        return await message.reply(f"<i><b>{ggl}Tidak ada broadcast yang berjalan!</b></i>")
    try:
        broadcasts.remove(client.me.id)
    except Exception:
        pass
    await message.reply(f"<i><b>{sks}Broadcast berhasil di hentikan!</b></i>")



async def bcfd_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    command, text = extract_type_and_msg(message)
    
    if command not in ["group", "channel", "users", "db", "all"] or not text:
        return await message.reply(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>type [reply]</b></i>")

    if not message.reply_to_message:
        return await message.reply(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>type [reply]</b></i>")
    broadcasts.append(client.me.id)
    msg_ = f"""<b><i>{prs}{prs_gcst}</i></b>"""
    try:
        x = await client.get_inline_bot_results(bot.me.username, f"broadcast|{client.me.id}|{msg_}")
        if not x.results:
            msg = await message.reply(msg_)
        else:
            msg = await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    except (ChatSendInlineForbidden, BotResponseTimeout, QueryIdInvalid):
        msg = await message.reply(msg_)
    except (ChatForbidden, Forbidden):
        pass
    chats = await get_data_id(client, command)
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    hasil = []
    for chat_id in chats:
        if chat_id in await db.get_list_from_vars(client.me.id, "bcdb"):
            if command == "db":
                try:
                    if client.me.id not in broadcasts:
                        break
                    await client.send_chat_action(chat_id, ChatAction.TYPING)
                    if message.reply_to_message:
                        await message.reply_to_message.forward(chat_id)
                    else:
                        await text.forward(chat_id)
                    done += 1
                except (ChannelPrivate, SlowmodeWait, Forbidden, ChatWriteForbidden, UserBannedInChannel, PeerIdInvalid) as e:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    try:
                        await client.send_chat_action(chat_id, ChatAction.TYPING)
                        if message.reply_to_message:
                            await message.reply_to_message.forward(chat_id)
                        else:
                            await text.forward(chat_id)
                        done += 1
                        if client.me.id not in broadcasts:
                            break
                    except Exception:
                       failed += 1
                except Exception:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            if message.reply_to_message:
                await message.reply_to_message.forward(chat_id)
            else:
                await text.forward(chat_id)
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                if message.reply_to_message:
                    await message.reply_to_message.forward(chat_id)
                else:
                    await text.forward(chat_id)
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts:
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    else:
        broadcasts.remove(client.me.id)
        try:
            await client.delete_messages(message.chat.id, (msg.updates[0].id or msg.id))
        except:
            pass
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass

async def bcfd_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    _msg = f"""<b><i>{prs}{prs_gcst}</i></b>"""
    gcs = await message.reply(_msg)

    command, text = extract_type_and_msg(message)
    
    if command not in ["group", "channel", "users", "db", "all"] or not text:
        return await gcs.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>type [reply]</b></i>")

    if not message.reply_to_message:
        broadcasts.remove(client.me.id)
        return await gcs.edit(f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>type [reply]</b></i>")
    broadcasts.append(client.me.id)
    chats = await get_data_id(client, command)
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    hasil = []
    for chat_id in chats:
        if chat_id in await db.get_list_from_vars(client.me.id, "bcdb"):
            if command == "db":
                try:
                    if client.me.id not in broadcasts:
                        break
                    await client.send_chat_action(chat_id, ChatAction.TYPING)
                    if message.reply_to_message:
                        await message.reply_to_message.forward(chat_id)
                    else:
                        await text.forward(chat_id)
                    done += 1
                except (ChannelPrivate, SlowmodeWait, Forbidden, ChatWriteForbidden, UserBannedInChannel, PeerIdInvalid) as e:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    try:
                        await client.send_chat_action(chat_id, ChatAction.TYPING)
                        if message.reply_to_message:
                            await message.reply_to_message.forward(chat_id)
                        else:
                            await text.forward(chat_id)
                        done += 1
                        if client.me.id not in broadcasts:
                            break
                    except Exception:
                       failed += 1
                except Exception:
                    failed += 1
                    try:
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except ChannelPrivate as e:
                        pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        chat = await client.get_chat(chat_id)
                        hasil.append((chat.title, chat.id))
                    except Exception as e:
                        pass
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue
        try:
            if client.me.id not in broadcasts:
                break
            await client.send_chat_action(chat_id, ChatAction.TYPING)
            if message.reply_to_message:
                await message.reply_to_message.forward(chat_id)
            else:
                await text.forward(chat_id)
            done += 1
        except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await client.send_chat_action(chat_id, ChatAction.TYPING)
                if message.reply_to_message:
                    await message.reply_to_message.forward(chat_id)
                else:
                    await text.forward(chat_id)
                done += 1
                if client.me.id not in broadcasts:
                    break
            except Exception:
                failed += 1
        except Exception:
            failed += 1
            try:
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except ChannelPrivate as e:
                pass
            except FloodWait as e:
                await asyncio.sleep(e.value)
                chat = await client.get_chat(chat_id)
                hasil.append((chat.title, chat.id))
            except Exception as e:
                pass
    if client.me.id not in broadcasts: 
        await gcs.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    else:
        await gcs.delete()
        await eor(message, f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> {command}</i>""")
    try:
        if failed:
            logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
            potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
            for anunya in potongan:
                await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
        else:
            await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
    except Exception as e:
        pass


@USU.UBOT("bcfd")
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await bcfd_inline(client, message)
    else:
        await bcfd_ori(client, message)


@USU.BOT("broadcast")
@USU.DEVS
async def _(client, message):
    msg = await message.reply(f"<i><b>Processing...</b></i>", quote=True)

    send = get_message(message)
    if not send:
        return await msg.edit(f"<b><i>Mohon balas atau ketik sesuatu...</i></b>")
        
    group = await db.get_list_from_vars(client.me.id, "group")
    user = await db.get_list_from_vars(client.me.id, "user")
    list_media = []
    done = 0
    if message.reply_to_message and message.reply_to_message.media_group_id:
        try:
            target = await client.get_media_group(message.chat.id, message.reply_to_message.id)
            for medianya in target:
                if medianya.photo:
                    list_media.append(InputMediaPhoto(media=medianya.photo.file_id, caption=medianya.caption, caption_entities=medianya.caption_entities))
                elif medianya.video:
                    list_media.append(InputMediaPhoto(media=medianya.video.file_id, caption=medianya.caption, caption_entities=medianya.caption_entities))
        except Exception as e:
            return await msg.edit(e)
    if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
        for chat_id in group:
            try:
                if message.reply_to_message:
                    if message.reply_to_message.media_group_id:
                        await client.send_media_group(chat_id, list_media)
                    elif message.reply_to_message.photo:
                        if send.reply_markup:
                            await client.send_photo(chat_id=chat_id, photo=message.reply_to_message.photo.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    elif message.reply_to_message.video:
                        if send.reply_markup:
                            await client.send_video(chat_id=chat_id, photo=message.reply_to_message.video.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    else:
                        if send.reply_markup:
                            await client.send_message(chat_id=chat_id, text=message.reply_to_message.text, entities=message.reply_to_message.entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                if message.reply_to_message:
                    if message.reply_to_message.media_group_id:
                        await client.send_media_group(chat_id, list_media)
                    elif message.reply_to_message.photo:
                        if send.reply_markup:
                            await client.send_photo(chat_id=chat_id, photo=message.reply_to_message.photo.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    elif message.reply_to_message.video:
                        if send.reply_markup:
                            await client.send_video(chat_id=chat_id, photo=message.reply_to_message.video.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    else:
                        if send.reply_markup:
                            await client.send_message(chat_id=chat_id, text=message.reply_to_message.text, entities=message.reply_to_message.entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
            except Exception as e:
                pass
            hasilnya = f"<i><b>Pesan broadcast berhasil terkirim ke {done} group</b></i>"
    else:
        for chat_id in user:
            try:
                if message.reply_to_message:
                    if message.reply_to_message.media_group_id:
                        await client.send_media_group(chat_id, list_media)
                    elif message.reply_to_message.photo:
                        if send.reply_markup:
                            await client.send_photo(chat_id=chat_id, photo=message.reply_to_message.photo.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    elif message.reply_to_message.video:
                        if send.reply_markup:
                            await client.send_video(chat_id=chat_id, photo=message.reply_to_message.video.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    else:
                        if send.reply_markup:
                            await client.send_message(chat_id=chat_id, text=message.reply_to_message.text, entities=message.reply_to_message.entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                if message.reply_to_message:
                    if message.reply_to_message.media_group_id:
                        await client.send_media_group(chat_id, list_media)
                    elif message.reply_to_message.photo:
                        if send.reply_markup:
                            await client.send_photo(chat_id=chat_id, photo=message.reply_to_message.photo.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    elif message.reply_to_message.video:
                        if send.reply_markup:
                            await client.send_video(chat_id=chat_id, photo=message.reply_to_message.video.file_id, caption=message.reply_to_message.caption, 
caption_entities=message.reply_to_message.caption_entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                    else:
                        if send.reply_markup:
                            await client.send_message(chat_id=chat_id, text=message.reply_to_message.text, entities=message.reply_to_message.entities, reply_markup=message.reply_to_message.reply_markup)
                        else:
                            await send.forward(chat_id)
                else:
                    await client.send_message(chat_id, send)
                done += 1
            except Exception as e:
                pass
            hasilnya = f"<i><b>Pesan broadcast berhasil terkirim ke {done} pengguna</b></i>"
    return await msg.edit(hasilnya)


AG = []
LT = []


@USU.UBOT("autobc")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    men = await EMO.MENUNGGU(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<b><i>{prs}Processing...</i></b>")
    type, value = extract_type_and_text(message)
    auto_text_vars = await db.get_vars(client.me.id, "AUTO_TEXT")

    if type == "on":
        if not auto_text_vars:
            return await msg.edit(
                f"<i><b>{ggl}Harap setting text dahulu!</b></i>"
            )

        if client.me.id not in AG:
            await msg.edit(f"<i><b>{sks}Auto broadcast on!</b></i>")

            AG.append(client.me.id)
            failed = 0
            hasil = []
            done = 0
            while client.me.id in AG:
                delay = await db.get_vars(client.me.id, "DELAY_GCAST") or 1
                chats = await get_data_id(client, "group")
                blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")
                txt = random.choice(auto_text_vars)

                group = 0
                for chat_id in chats:
                    if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
                        continue
                    try:
                        await client.send_chat_action(chat_id, ChatAction.TYPING)
                        await client.send_message(chat_id, f"{txt} ")
                        group += 1
                        await asyncio.sleep(0.5)
                    except (ChannelPrivate, SlowmodeWait, ChatWriteForbidden, Forbidden, UserBannedInChannel, PeerIdInvalid) as e:
                        failed += 1
                        try:
                            chat = await client.get_chat(chat_id)
                            hasil.append((chat.title, chat.id))
                        except ChannelPrivate as e:
                            pass
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            chat = await client.get_chat(chat_id)
                            hasil.append((chat.title, chat.id))
                        except Exception as e:
                            pass
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                        try:
                            await client.send_chat_action(chat_id, ChatAction.TYPING)
                            await client.send_message(chat_id, f"{txt} ")
                            group += 1
                        except Exception:
                            failed += 1
                    except Exception:
                        failed += 1
                        try:
                            chat = await client.get_chat(chat_id)
                            hasil.append((chat.title, chat.id))
                        except ChannelPrivate as e:
                            pass
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            chat = await client.get_chat(chat_id)
                            hasil.append((chat.title, chat.id))
                        except Exception as e:
                            pass

                if client.me.id not in AG:
                    return

                done += 1
                await msg.reply(f"""<i><b>{broad}Auto Broadcast!</b>
<b>{sks}Success:</b> {group}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Putaran:</b> {done}
<b>{men}Wait:</b> {delay} <b>Minutes</b></i>""",
                    quote=True,
                )
                try:
                    if failed:
                        logs_hasil = "Failed Broadcast!\n\n" + "\n".join(f"{title_group} | {id_group}" for title_group, id_group in hasil)
                        potongan = [logs_hasil[i:i + 4096] for i in range(0, len(logs_hasil), 4096)]
                        for anunya in potongan:
                            await bot.send_message(client.me.id, f"<i><b>{anunya}</b></i>")
                    else:
                       await bot.send_message(client.me.id, f"<i><b>All broadcasts were sent successfully!</b></i>")
                except Exception as e:
                    pass
                await asyncio.sleep(int(60) * int(delay))
        else:
            return await msg.edit(f"<i><b>Auto broadcast sudah on sebelumnya!</b></i>")

    elif type == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            return await msg.edit(f"<i><b>{sks}Auto broadcast off!</b></i>")
        else:
            return await msg.edit(f"<i><b>{ggl}Auto broadcast sudah off sebelumnya!</b></i>")

    elif type == "text":
        if not value:
            return await msg.edit(
                f"<i><b>{ggl}<code>{message.text.split()[0]} text</code> - [value]</b></i>"
            )
        await add_auto_text(client, value)
        return await msg.edit(f"<i><b>{sks}Text saved!</b></i>")

    elif type == "delay":
        if not int(value):
            return await msg.edit(
                f"<i><b>{ggl}<code>{message.text.split()[0]} delay</code> - [value]</b></i>"
            )
        await db.set_vars(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(
            f"<i><b>{sks}Success set {value} minute</b></i>"
        )

    elif type == "remove":
        if not value:
            return await msg.edit(
                f"<i><b>{ggl}<code>{message.text.split()[0]} remove</code> - [value]</b></i>"
            )
        if value == "all":
            await db.set_vars(client.me.id, "AUTO_TEXT", [])
            return await msg.edit(f"<b><i>{sks}Clear text!</i></b>")
        try:
            value = int(value) - 1
            auto_text_vars.pop(value)
            await db.set_vars(client.me.id, "AUTO_TEXT", auto_text_vars)
            return await msg.edit(
                f"<i><b>{sks}Text {value+1} deleted!</b></i>"
            )
        except Exception as error:
            return await msg.edit(str(error))

    elif type == "list":
        if not auto_text_vars:
            return await msg.edit(f"<i><b>{ggl}Empty!</b></i>")
        txt = "<b>Daftar auto broadcast text!</b>\n\n"
        for num, x in enumerate(auto_text_vars, 1):
            txt += f"<b>{num}•></b> {x}\n\n"
        txt += f"<b>\nUntuk menghapus text:\n<code>{message.text.split()[0]} remove</code> [angka/all]</b>"
        return await msg.edit(f"<i>{txt}</i>")

    elif type == "limit":
        if value == "off":
            if client.me.id in LT:
                LT.remove(client.me.id)
                return await msg.edit(f"<i><b>{sks}Auto check limit off!</b></i>")
            else:
                return await msg.edit(f"<i><b>{ggl}Auto check limit sudah off sebelumnya!</b></i>")

        elif value == "on":
            if client.me.id not in LT:
                LT.append(client.me.id)
                await msg.edit(f"<i><b>{sks}Auto check limit on!</b></i>")
                while client.me.id in LT:
                    for x in range(2):
                        await limit_cmd(client, message)
                        await asyncio.sleep(5)
                    await asyncio.sleep(1200)
            else:
                return await msg.edit(f"<i><b>{ggl}Auto check limit sudah on sebelumnya!</b></i>")
        else:
             return await msg.edit(f"<i><b>{ggl}<code>{message.text.split()[0]} limit</code> - [value]</b></i>")

    else:
        return await msg.edit(f"<i><b>{ggl}<code>{message.text.split()[0]}</code> [query] - [value]</b></i>")


async def add_auto_text(client, text):
    auto_text = await db.get_vars(client.me.id, "AUTO_TEXT") or []
    auto_text.append(text)
    await db.set_vars(client.me.id, "AUTO_TEXT", auto_text)

