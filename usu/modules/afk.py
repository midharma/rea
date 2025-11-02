from usu import *




@USU.UBOT("afk")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    reason = get_arg(message)
    db_afk = {"time": time(), "reason": reason}
    msg_afk = (
        f"<b><i>{sks}Afk!\n{broad}Reason: {reason}</i></b>"
        if reason
        else f"<b><i>{sks}Afk!</i></b>"
      )
    await db.set_vars(client.me.id, "AFK", db_afk)
    return await message.reply(msg_afk)



@USU.NO_CMD("AFK", ubot)
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    menu = await EMO.MENUNGGU(client)
    vars = await db.get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_reason = vars.get("reason")
        afk_runtime = await get_time(time() - afk_time)
        afk_text = (
            f"<b><i>{sks}Afk!\n{ptr}Time: {afk_runtime}\n{broad}Reason: {afk_reason}</i></b>"
            if afk_reason
            else f"<b><i>{sks}Afk!\n{menu}Time: {afk_runtime}</i></b>"
        )
        try:
            await message.reply(afk_text)
        except pyrogram.errors.exceptions.forbidden_403.ChatWriteForbidden as e:
            print(e)
            return


@USU.UBOT("unafk")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    menu = await EMO.MENUNGGU(client)
    vars = await db.get_vars(client.me.id, "AFK")
    if vars:
        afk_time = vars.get("time")
        afk_runtime = await get_time(time() - afk_time)
        afk_text = f"<b><i>{sks}Online!\n{menu}Afk selama: {afk_runtime}</i></b>"
        await message.reply(afk_text)
        return await db.remove_vars(client.me.id, "AFK")

