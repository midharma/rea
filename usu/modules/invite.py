import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType, UserStatus

from usu import *




@USU.UBOT("invite")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    mg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if len(message.command) < 2:
        return await mg.delete()
    user_s_to_add = message.text.split(" ", 1)[1]
    if not user_s_to_add:
        await mg.edit(
            f"<i><b>{ggl}Invalid!</b></i>"
        )
        return
    user_list = user_s_to_add.split(" ")
    try:
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await client.add_chat_members(message.chat.id, user_list, forward_limit=100)
    except Exception as e:
        return await mg.edit(f"{e}")
    await mg.edit(f"<i><b>{sks}Success invite!</b></i>")



invite_id = {}


@USU.UBOT("inviteall")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Tm = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    await asyncio.sleep(2)
    if len(message.command) < 3:
        await message.delete()
        return await Tm.delete()
    queryy = message.text.split()[1]
    colldown = message.text.split()[2]
    chat = await client.get_chat(queryy)
    tgchat = message.chat
    if client.me.id in invite_id and tgchat.id in invite_id[client.me.id]:
        return await Tm.edit_text(
            f"<i><b>{ggl}Invalid!</b></i>"
        )
    else:
        if client.me.id not in invite_id:
            invite_id[client.me.id] = []
        invite_id[client.me.id].append(tgchat.id)
        done = 0
        async for member in client.get_chat_members(chat.id):
            user = member.user
            zxb = [
                UserStatus.ONLINE,
                UserStatus.OFFLINE,
                UserStatus.RECENTLY,
                UserStatus.LAST_WEEK,
            ]
            if user.status in zxb:
                try:
                    await client.add_chat_members(tgchat.id, user.id)
                    done += 1
                    await asyncio.sleep(int(colldown))
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await client.add_chat_members(tgchat.id, user.id)
                    done += 1
                    await asyncio.sleep(int(colldown))
                except Exception:
                    pass
        invite_id[client.me.id].remove(tgchat.id)
        await Tm.delete()
        return await eor(
            message,
            f"<i><b>{sks}Success invite {done}!</b></i>"
        )


@USU.UBOT("cancelinvite")
@USU.GROUP
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if client.me.id not in invite_id:
        return await message.reply_text(
            f"<i><b>{ggl}Invalid!</b></i>"
        )
    else:
        try:
            invite_id[client.me.id].remove(message.chat.id)
            await message.reply_text(f"<i><b>{sks}Success canceled!</b></i>")
        except Exception as e:
            await message.reply_text(e)


