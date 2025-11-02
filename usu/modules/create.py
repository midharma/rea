from usu import *




@USU.UBOT("creat")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) < 3:
        return await message.reply(
            f"<i><b>{ggl}<code>{message.text}</code> [name/title]</b></i>")
    group_type = message.command[1]
    split = message.command[2:]
    group_name = " ".join(split)
    xd = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    desc = "Welcome To My " + ("Group" if group_type == "group" else "Channel")
    if group_type == "group":
        _id = await client.create_supergroup(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"<i><b>{sks}Success: [{group_name}]({link.invite_link})</b></i>",
            disable_web_page_preview=True,
        )
    elif group_type == "channel":
        _id = await client.create_channel(group_name, desc)
        link = await client.get_chat(_id.id)
        await xd.edit(
            f"<i><b>{sks}Success: [{group_name}]({link.invite_link})</b></i>",
            disable_web_page_preview=True,
        )
