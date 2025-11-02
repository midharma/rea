from pyrogram import Client
from pyrogram import errors
from pyrogram import enums
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UserAlreadyParticipant
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

from pyrogram import *
from usu import *



@USU.UBOT("kickme")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    aio = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if message.chat.id in BLACKLIST_CHAT:
        return await xxnx.edit(f"<i><b>{ggl}Invalid!</b></i>")
    try:
        await xxnx.edit_text(f"<i><b>{sks}Successfully exit!</b></i>")
        await client.leave_chat(aio)
    except UserNotParticipant:
        await xxnx.edit_text(f"{ggl}Anda belum berada di chat tersebut!")
    except Exception as ex:
        await xxnx.edit_text(f"ERROR: \n\n{str(ex)}")



@USU.UBOT("join")
@ubot.on_message(filters.user(DEVS) & filters.command("cjoin", ""))
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    aio = message.command[1] if len(message.command) > 1 else message.chat.id
    xxnx = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    try:
        await xxnx.edit(f"<i><b>{sks}Successfully joined!</b></i>")
        await client.join_chat(aio)
    except UserAlreadyParticipant:
        await xxnx.edit(f"{ggl}Anda sudah berada di chat tersebut!")
    except Exception as ex:
        await xxnx.edit(f"{ggl}ERROR: \n\n{str(ex)}")


@USU.UBOT("leaveallgc")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Man = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"""<i><b>{broad}Leave Group!
{sks}Success: {done}
{ggl}Failed: {er}</b></i>"""
    )


@USU.UBOT("leaveallch")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Man = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    er = 0
    done = 0
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.CHANNEL):
            chat = dialog.chat.id
            try:
                done += 1
                await client.leave_chat(chat)
            except BaseException:
                er += 1
    await Man.edit(
        f"""<i><b>{broad}Leave Channel!
{sks}Success: {done}
{ggl}Failed: {er}</b></i>"""
    )

@USU.UBOT("leaveallmute")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    done = 0
    Man = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    async for dialog in client.get_dialogs():
        if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
            chat = dialog.chat.id
            try:
                member = await client.get_chat_member(chat, "me")
                if member.status == ChatMemberStatus.RESTRICTED:
                    await client.leave_chat(chat)
                    done += 1
            except Exception:
                pass
    await Man.edit(f"""<i><b>{sks}Out of {done} group!</b></i>""")


