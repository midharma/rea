from usu import *



ADDSUDO = """Command for <b>Add Sudo</b>

<b>Add Sudo</b>
 <i>menambahkan sudo user</i>
    <code>{0}addsudo</code>
   
<b>Notes:</b>
<i>pengguna yang di tambahkan bisa menggunakan bot anda sesuai prefix handler</i>"""

DELSUDO = """Command for <b>Delete Sudo</b>

<b>Delete Sudo</b>
 <i>menghapus sudo user</i>
    <code>{0}delsudo</code>"""

LISTSUDO = """Command for <b>List Sudo</b>

<b>List Sudo</b>
 <i>mendapatkan daftar sudo user</i>
    <code>{0}listsudo</code>"""

CLEARSUDO = """Command for <b>Clear Sudo</b>

<b>Clear Sudo</b>
 <i>menghapus semua sudo user</i>
    <code>{0}clearsudo</code>"""


__UTAMA__ = "Sudoers"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Add Sudo", "Delete Sudo", "List Sudo", "Clear Sudo"

__HASIL__ = ADDSUDO, DELSUDO, LISTSUDO, CLEARSUDO


@USU.UBOT("addsudo")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [user_id/username]</i></b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await db.get_list_from_vars(client.me.id, "SUDO_USERS")

    if user.id in sudo_users:
        return await msg.edit(
            f"<i><b>{ggl}Already in sudo!</b></i>"
        )

    try:
        await db.add_to_vars(client.me.id, "SUDO_USERS", user.id)
        return await msg.edit(
            f"<i><b>{sks}Added to sudo!</b></i>"
        )
    except Exception as error:
        return await msg.edit(error)


@USU.UBOT("delsudo")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [user_id/username]</i></b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await db.get_list_from_vars(client.me.id, "SUDO_USERS")

    if user.id not in sudo_users:
        return await msg.edit(
            f"<i><b>{ggl}Not in sudo!</b></i>"
        )

    try:
        await db.remove_from_vars(client.me.id, "SUDO_USERS", user.id)
        return await msg.edit(
            f"<i><b>{sks}Removed from sudo!</b></i>"
        )
    except Exception as error:
        return await msg.edit(error)


@USU.UBOT("listsudo")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Sh = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    sudo_users = await db.get_list_from_vars(client.me.id, "SUDO_USERS")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            sudo_list.append(
                f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>"
            )
        except:
            continue

    if sudo_list:
        response = (
            f"<b>{broad}Sudo:</b>\n"
            + "\n".join(sudo_list)
            + f"\n<b>{sks}Total sudo:</b> <code>{len(sudo_list)}</code>"
        )
        return await Sh.edit(f"<i>{response}</i>")
    else:
        return await Sh.edit(f"<i><b>{ggl}Empty!</b></i>")


@USU.UBOT("clearsudo")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"

    msg = await message.reply(_msg)
    sudo = await db.get_list_from_vars(client.me.id, "SUDO_USERS")

    if not sudo:
        return await msg.edit(f"<i><b>{ggl}Empty!</b></i>")

    for chat_id in sudo:
        await db.remove_from_vars(client.me.id, "SUDO_USERS", chat_id)

    await msg.edit(f"<i><b>{sks}Clear sudo!</b></i>")


#=================


@USU.BOT("addsudo")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [user_id/username]</i></b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await db.get_list_from_vars(bot.me.id, "SUDO")

    if user.id in sudo_users:
        return await msg.edit(
            f"<i><b>{ggl}Already in sudo!</b></i>"
        )

    try:
        await db.add_to_vars(bot.me.id, "SUDO", user.id)
        return await msg.edit(
            f"<i><b>{sks}Added to sudo!</b></i>"
        )
    except Exception as error:
        return await msg.edit(error)


@USU.BOT("delsudo")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b><i>{ggl}<code>{message.text.split()[0]}</code> [user_id/username]</i></b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await db.get_list_from_vars(bot.me.id, "SUDO")

    if user.id not in sudo_users:
        return await msg.edit(
            f"<i><b>{ggl}Not in sudo!</b></i>"
        )

    try:
        await db.remove_from_vars(bot.me.id, "SUDO", user.id)
        return await msg.edit(
            f"<i><b>{sks}Removed from sudo!</b></i>"
        )
    except Exception as error:
        return await msg.edit(error)


@USU.BOT("listsudo")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    Sh = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    sudo_users = await db.get_list_from_vars(bot.me.id, "SUDO")

    sudo_list = []
    for user_id in sudo_users:
        try:
            user = await client.get_users(int(user_id))
            sudo_list.append(
                f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code>"
            )
        except:
            continue

    if sudo_list:
        response = (
            f"<b>{broad}Sudo:</b>\n"
            + "\n".join(sudo_list)
            + f"\n<b>{sks}Total sudo:</b> <code>{len(sudo_list)}</code>"
        )
        return await Sh.edit(f"<i>{response}</i>")
    else:
        return await Sh.edit(f"<i><b>{ggl}Empty!</b></i>")


@USU.BOT("clearsudo")
@USU.DEVS
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    _msg = f"<b><i>{prs}Processing...</i></b>"

    msg = await message.reply(_msg)
    sudo = await db.get_list_from_vars(bot.me.id, "SUDO")

    if not sudo:
        return await msg.edit(f"<i><b>{ggl}Empty!</b></i>")

    for chat_id in sudo:
        await db.remove_from_vars(bot.me.id, "SUDO", chat_id)

    await msg.edit(f"<i><b>{sks}Clear sudo!</b></i>")
