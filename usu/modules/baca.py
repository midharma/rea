from usu import *





@USU.UBOT("baca|read")
async def baca_read(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    usu = await message.reply_text(f"<i><b>{prs}Processing...</b></i>")
    cmd = message.text.split()

    if len(cmd) < 2:
        return await usu.edit_text(f"<i><b>{ggl}{message.text.split()[0]} [group/users/channel/all]</i></b>")

    if cmd[1] not in {"group", "users", "channel", "all"}:
        return await usu.edit_text(f"<i><b>{ggl}{message.text.split()[0]} [group/users/channel/all]</i></b>")
    query = cmd[1]
    chats = await get_data_id(client, query)
    done = 0
    for dialog in chats:
        if dialog:
            try:
                sukses = await client.read_chat_history(dialog)
                if sukses:
                    done += 1
            except ChannelPrivate:
                continue
            except Exception as e:
                await usu.edit_text(f"{ggl} Error: {str(e)}")
                return
    await usu.edit_text(f"""<i><b>{broad}Read Chat!
{sks}Success: {done}
{ptr}Type: {query}</b></i>""")