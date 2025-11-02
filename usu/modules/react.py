

from usu import *
from pyrogram import Client, idle, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import ChatMember
from pyrogram.errors.exceptions import UserNotParticipant


@USU.UBOT("react")
async def _(c, m):
    sks = await EMO.SUKSES(c)
    ggl = await EMO.GAGAL(c)
    prs = await EMO.PROSES(c)
    broad = await EMO.BROADCAST(c)
    ptr = await EMO.PUTARAN(c)
    global reaction_progress
    reaction_progress = True
    try:
        if len(m.command) != 3:
            return await m.reply(f"<i><b>{ggl}Invalid!</b><i>")

        chat_id = m.command[1]
    except IndexError:
        await m.reply(f"<i><b>{ggl}Invalid!</b></i>")
        return

    rach = await m.reply(f"<i><b>{prs}Processing...</b></i>")
    async for message in c.get_chat_history(chat_id):
        await asyncio.sleep(0.5)
        chat_id = message.chat.id
        message_id = message.id
        try:
            if not reaction_progress:
                break
            await asyncio.sleep(0.5)
            await c.send_reaction(chat_id=chat_id, message_id=message_id, emoji=m.command[2])
        except Exception:
            pass
    
    await rach.edit(f"<i><b>{sks}Success reaction!</b></i>")


@USU.UBOT("cancelreact")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    global reaction_progress
    reaction_progress = False
    await message.reply(f"<i><b>{sks}Successfully canceled!</b></i>")
