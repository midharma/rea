from pyrogram.enums import ChatType
from asyncio import sleep

from usu import *



@USU.UBOT("archiveall")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    done = 0
    gagal = 0
    usu = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")

    if len(message.command) != 2:
        await usu.edit(f"<b><i>{ggl}{message.text} Type</i></b>")
        return

    query = message.command[1]

    chat_ids = await get_data_id(client, query)

    for chat_id in chat_ids:
        await sleep(1)
        try:
            await client.archive_chats(chat_id)
            done += 1
        except:
            gagal += 1
            pass

    await usu.edit(f"""<i><b>{broad}Archive!
{sks}Success: {done}
{ggl}Failed: {gagal}</b></i>""")


@USU.UBOT("unarchiveall")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    done = 0
    gagal = 0
    usu = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")

    if len(message.command) != 2:
        await usu.edit(f"<b><i>{ggl}{message.text} Type</i></b>")
        return

    query = message.command[1]

    chat_ids = await get_data_id(client, query)

    for chat_id in chat_ids:
        await sleep(1)
        try:
            await client.unarchive_chats(chat_id)
            done += 1
        except:
            gagal += 1
            pass

    await usu.edit(f"""<i><b>{broad}Unarchive!
{sks}Success: {done}
{ggl}Failed: {gagal}</b></i>""")
