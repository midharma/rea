import asyncio

from pyrogram.enums import ChatType, ChatAction
from pyrogram.errors import (
    FloodWait,
    ChannelPrivate,
    SlowmodeWait,
    ChatWriteForbidden,
    Forbidden,
    UserBannedInChannel,
    PeerIdInvalid,
    QueryIdInvalid,
    ChatForbidden,
    ChatSendInlineForbidden,
    BotResponseTimeout
)

from .. import *



spam = []
spamg = []



async def SpamMsg(client, message, send):
    delay = await db.get_vars(client.me.id, "SPAM") or 0
    try:
        await asyncio.sleep(int(delay)) 
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        if message.reply_to_message:
            await send.copy(message.chat.id)
        else:
            await client.send_message(message.chat.id, send)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
        if message.reply_to_message:
            await send.copy(message.chat.id)
        else:
            await client.send_message(message.chat.id, send)



async def SpamGcast(client, message, send, hasil, done, failed):
    blacklist = await db.get_list_from_vars(client.me.id, "BL_ID")

    async def send_message(target_chat):
        await client.send_chat_action(target_chat, ChatAction.TYPING)
        if message.reply_to_message:
            await send.copy(target_chat)
        else:
            await client.send_message(target_chat, send)

    async def handle_flood_wait(exception, target_chat):
        await asyncio.sleep(exception.value)
        await client.send_chat_action(target_chat, ChatAction.TYPING)
        await send_message(target_chat)

    async for dialog in client.get_dialogs():
        if (
            dialog.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
            and dialog.chat.id not in blacklist
        ):
            try:
                if client.me.id not in spamg:
                    break
                await send_message(dialog.chat.id)
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
                await handle_flood_wait(e, dialog.chat.id)
                done += 1
                if client.me.id not in spamg:
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


@USU.UBOT("spam")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<i><b>{prs}Processing...</b></i>"
    spam.append(client.me.id)
    r = await message.reply(_msg)
    count, msg = extract_type_and_msg(message)

    try:
        count = int(count)
    except Exception:
        return await r.edit(f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [Jumlah] [Text/Reply]</i></b>")

    if not msg:
        spam.remove(client.me.id)
        return await r.edit(
            f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [Jumlah] [Text/Reply]</b></i>"
        )
    for _ in range(count):
        if client.me.id not in spam:
            break
        await SpamMsg(client, message, msg)

    if client.me.id not in spam:
        return await r.delete()    
    else:
        spam.remove(client.me.id)
        return await r.delete()


@USU.UBOT("cancelspam")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if client.me.id not in spam:
        return await message.reply(f"<i><b>{ggl}Tidak ada spam message</b></i>")
    try:
        spam.remove(client.me.id)
    except Exception:
        pass
    await message.reply(f"<i><b>{sks}Spam message berhasil di hentikan</b></i>")


async def spamg_inline(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    wkt = await EMO.MENUNGGU(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    msg_ = f"<i><b>{prs}{prs_gcst}</b></i>"

    count, msg = extract_type_and_msg(message)

    try:
        count = int(count)
    except Exception:
        return await message.reply(f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [Jumlah] [Text/Reply]</i></b>")

    if not msg:
        return await message.reply(
            f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [Jumlah] [Text/Reply]</i></b>"
        )
    done = 0
    failed = 0
    hasil = []
    spamg.append(client.me.id)
    x = await client.get_inline_bot_results(bot.me.username, f"broadcast {client.me.id} {msg_}")
    if not x.results:
        anu = await message.reply(msg_)
    else:
        anu = await message.reply_inline_bot_result(x.query_id, x.results[0].id)
    async def run_spam():
        spam_gcast = [SpamGcast(client, message, msg, hasil, done, failed) for _ in range(int(count))]
        await asyncio.gather(*spam_gcast)

    await run_spam()
    if client.me.id not in spamg:
        await client.delete_messages(message.chat.id, anu.updates[0].id)
        await message.reply(f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group
<b>{wkt}Count:</b> {count}</i>""")
    else:
        spamg.remove(client.me.id)
        await client.delete_messages(message.chat.id, anu.updates[0].id)
        await message.reply(f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group
<b>{wkt}Count:</b> {count}</i>""")
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


async def spamg_ori(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    wkt = await EMO.MENUNGGU(client)
    prs_gcst = await TEXT.PROSES(client)
    broad_gcst = await TEXT.BROADCAST(client)
    msg_ = await message.reply(f"<i><b>{prs}{prs_gcst}</b></i>")
    count, msg = extract_type_and_msg(message)

    try:
        count = int(count)
    except Exception:
        return await message.reply(f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [Jumlah] [Text/Reply]</i></b>")

    if not msg:
        return await message.reply(
            f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [Jumlah] [Text/Reply]</i></b>"
        )
    done = 0
    failed = 0
    hasil = []
    spamg.append(client.me.id)
    async def run_spam():
        spam_gcast = [SpamGcast(client, message, msg, hasil, done, failed) for _ in range(int(count))]
        await asyncio.gather(*spam_gcast)

    await run_spam()
    if client.me.id not in spamg:
        await msg_.delete()
        await message.reply(f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group
<b>{wkt}Count:</b> {count}</i>""")
    else:
        spamg.remove(client.me.id)
        await msg_.delete()
        await message.reply(f"""<i><b>{broad}{broad_gcst}</b>
<b>{sks}Success:</b> {done}
<b>{ggl}Failed:</b> {failed}
<b>{ptr}Type:</b> group
<b>{wkt}Count:</b> {count}</i>""")
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


@USU.UBOT("spamg")
async def _(client, message):
    vars = await db.get_vars(client.me.id, "inline")
    if vars:
        await spamg_inline(client, message)
    else:
        await spamg_ori(client, message)


@USU.UBOT("cancelspamg")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if client.me.id not in spamg:
        return await message.reply(f"<i><b>{ggl}Tidak ada spam gcast</b></i>")
    try:
        spamg.remove(client.me.id)
    except Exception:
        pass
    await message.reply(f"<i><b>{sks}Spam gcast berhasil di hentikan</b></i>")


@USU.UBOT("setdelay")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<i><b>{prs}Processing...</b></i>"

    r = await message.reply(_msg)

    if len(message.command) != 2:
        return await r.edit(f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [angka/none]</i></b>")

    count = message.command[1]

    if count.lower() == "none":
        await db.set_vars(client.me.id, "SPAM", False)
        return await r.edit(f"<b><i>{sks}Spam delay di settings ke Default</i></b>")
    try:
        count = int(count)
    except Exception:
        return await r.edit(f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [angka]</i></b>")

    await db.set_vars(client.me.id, "SPAM", count)
    return await r.edit(f"<b><i>{sks}Spam delay di settings ke {count}</i></b>")