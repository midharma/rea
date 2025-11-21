from pyrogram import Client
from pyrogram import errors
from pyrogram import enums
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UserAlreadyParticipant
import asyncio

from pyrogram import *
from usu import *

from pyrogram.raw.functions.messages import DeleteHistory



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
        await xxnx.edit_text(f"<b><i>{ggl}Anda belum berada di chat tersebut!</i></b>")
    except Exception as ex:
        await xxnx.edit_text(f"ERROR: \n\n{str(ex)}")



@USU.UBOT("join")
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
        await xxnx.edit(f"<b><i>{ggl}Anda sudah berada di chat tersebut!</i></b>")
    except Exception as ex:
        await xxnx.edit(f"{ggl}ERROR: \n\n{str(ex)}")




@USU.UBOT("leaveall")
async def leave_all(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    usu = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")
    cmd = message.text.split()
    if len(cmd) < 2:
        return await usu.edit_text(f"<i><b>{ggl}{message.text.split()[0]} [group/users/channel/all]</i></b>")
    if cmd[1] not in {"group", "mute", "channel", "users"}:
        return await usu.edit_text(f"<i><b>{ggl}{message.text.split()[0]} [group/users/channel/all]</i></b>")
    done = 0
    er = 0
    if cmd[1] == "mute":
        async for dialog in client.get_dialogs():
            if dialog.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP):
                chat = dialog.chat.id
                try:
                    member = await client.get_chat_member(chat, "me")
                    if member.status == ChatMemberStatus.RESTRICTED:
                        await client.leave_chat(chat)
                        done += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    member = await client.get_chat_member(chat, "me")
                    if member.status == ChatMemberStatus.RESTRICTED:
                        await client.leave_chat(chat)
                        done += 1
                except Exception:
                    er += 1
    elif cmd[1] == "users":
        chats = await get_data_id(client, cmd[1])
        for dialog in chats:
            if dialog:
                peer = await client.resolve_peer(dialog.chat.id)
                try:
                    await client.invoke(
                        DeleteHistory(
                        peer=peer,
                        max_id=0,
                        revoke=True
                        )
                    )
                    done += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await client.invoke(
                        DeleteHistory(
                        peer=peer,
                        max_id=0,
                        revoke=True
                        )
                    )
                    done += 1
                except Exception as e:
                    er += 1
    else:
        chats = await get_data_id(client, cmd[1])
        for dialog in chats:
            if dialog:
                chat = dialog.chat.id
                try:
                    await client.leave_chat(chat)
                    done += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await client.leave_chat(chat)
                    done += 1
                except Exception as e:
                    er += 1
    await usu.edit_text(f"""<i><b>{broad}Keluar Chat!
{sks}Success: {done}
{ggl}Failed: {er}
{ptr}Type: {cmd[1]}</b></i>""")


