from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from pyrogram.raw.functions.auth import LogOut

from usu import *
from usu.config import HARGA_USERBOT


@USU.BOT("delubot")
@USU.DEVS
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<i><b>{message.text} user_id/username</b></i>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    if user.id in ubot._ubot:
        try:
            X = ubot._ubot[user.id]
            try:
                await X.unblock_user(bot.me.username)
            except Exception as e:
                pass
            await db.remove_ubot(user.id)
            await db.rem_expired_date(user.id)
            await msg.edit(f"<i><b>Successfully removed!</b></i>")
            try:
                await X.invoke(LogOut())
            except:
                pass
            del ubot._ubot[user.id]
        except Exception as e:
            await msg.edit(e)
    else:
        return await msg.edit(f"<i><b>Not client!</b></i>")


@USU.BOT("getubot")
@USU.DEVS
@USU.PRIVATE
async def _(client, message):
    await bot.send_message(
        message.chat.id,
        await MSG.UBOT(0),
        reply_markup=InlineKeyboardMarkup(BTN.UBOT(ubot._ubot[tuple(ubot._ubot.keys())[0]].me.id, 0)),
    )


@USU.BOT("seles")
@USU.DEVS
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<i><b>{message.text} user_id/username</b></i>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await db.get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id in sudo_users:
        return await msg.edit(f"""<i><b>Invalid!</b></i>
"""
        )

    try:
        await db.add_to_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>ID:</b> <code>{user.id}</code>
 <b>Status:</b> seles</i>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@USU.BOT("delseles")
@USU.DEVS
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<i><b>{message.text} user_id/username</b></i>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await db.get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id not in seles_users:
        return await msg.edit(f"""<i><b>Invalid!</b></i>
"""
        )

    try:
        await db.remove_from_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>ID:</b> <code>{user.id}</code>
 <b>Status:</b> unseles</i>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@USU.BOT("getseles")
@USU.DEVS
async def _(client, message):
    Sh = await eor(message, f"<i><b>Processing...</b></i>")
    seles_users = await db.get_list_from_vars(client.me.id, "SELER_USERS")

    if not seles_users:
        return await Sh.edit(f"<i><b>Empty!</b></i>")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except:
            continue

    if seles_list:
        response = (
            "<i><b>Daftar seles:</b>\n\n"
            + "\n".join(seles_list)
            + f"\n\n<b>Total seles:</b> <code>{len(seles_list)}</code></i>"
        )
        return await Sh.edit(response)


@USU.BOT("cek")
@USU.SELLER
async def _(client, message):
    Sh = await eor(message, f"<i><b>Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await Sh.edit(f"<i><b>Invalid!</b></i>")
    try:
        get_exp = await db.get_expired_date(user_id)
        sh = await client.get_users(user_id)
        SH = await ubot.get_prefix(user_id)
        if get_exp is None:
            exp = "None"
        else:
            exp = get_exp.strftime("%d %B %Y")
    except Exception as error:
        return await Sh.edit(error)
    vars = await db.get_vars(sh.id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{saldo:,}".replace(",", ".")
    if user_id in ubot._ubot:
        await Sh.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {sh.mention}
 <b>ID:</b> <code>{sh.id}</code>
 <b>Prefix:</b> {' '.join(SH)}
 <b>Masa Aktif:</b> {exp}
 <b>Saldo Userbot:</b> Rp {teks}</i>
"""
        )
    elif user_id in await db.get_list_from_vars(client.me.id, "AKSES"):
        await Sh.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {sh.mention}
 <b>ID:</b> <code>{sh.id}</code>
 <b>Prefix:</b> None
 <b>Masa Aktif:</b> {exp}
 <b>Saldo Userbot:</b> Rp {teks}</i>
"""
        )        
    else:
        await Sh.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {sh.mention}
 <b>ID:</b> <code>{sh.id}</code>
 <b>Prefix:</b> None
 <b>Masa Aktif:</b> {exp}
 <b>Saldo Userbot:</b> Rp {teks}</i>
"""
        )


@USU.BOT("time")
@USU.SELLER
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    replied = message.reply_to_message
    usu = message.command

    try:
        if replied:
            user_id = replied.from_user.id
            if len(usu) > 1 and usu[1].isdigit():
                get_day = int(usu[1])
            else:
                get_day = 30
        elif len(usu) > 1:
            if usu[1].isdigit():
                user_id = int(usu[1])
            else:
                try:
                    user_id = (await client.resolve_peer(usu[1])).user_id
                except Exception as error:
                    return await msg.edit(error)
            if len(usu) > 2 and usu[-1].isdigit():
                get_day = int(usu[-1])
            else:
                get_day = 30
        else:
            return await msg.edit(f"<i><b>{message.text} user_id/username - hari</b></i>")
    except Exception as error:
        return await msg.edit(error)

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    jakarta_timezone = pytz.timezone("Asia/Jakarta")
    now = datetime.now(jakarta_timezone)
    expire_date = now + timedelta(days=int(get_day))
    if user_id in ubot._ubot or user_id in await db.get_list_from_vars(client.me.id, "AKSES"):
        await db.set_expired_date(user_id, expire_date)
        await msg.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>ID:</b> <code>{user.id}</code>
 <b>Expired:</b> {get_day} hari</i>
"""
        )
    else:
        return await msg.edit(f"""<i><b>Not client!</b></i>
"""
        )
    try:
        for semua in DEVS:
            await bot.send_message(
                semua,
                f"<i><b>ID-Seller:</b> <code>{message.from_user.id}</code>\n<b>ID-Customer:</b> <code>{user.id}</code>\n<b>Masa Aktif:</b> {get_day} hari</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                            f"{message.from_user.first_name} {message.from_user.last_name or ''}",
                            url=f"tg://openmessage?user_id={message.from_user.id}",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                f"{user.first_name} {user.last_name or ''}",     url=f"tg://openmessage?user_id={user.id}"
                            ),
                        ],
                    ]
                ),
            )
    except Exception as error:
        return await msg.edit(error)




@USU.BOT("getuser")
@USU.SELLER
async def _(client, message):
    tt = await eor(message, f"Processing...")
    xx = len(ubot._ubot)
    await tt.edit(f"<i><b>Client:</b> {xx}</i>")


@USU.BOT("delakses")
@USU.SELLER
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<i><b>{message.text} user_id/username</b></i>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await db.get_list_from_vars(client.me.id, "AKSES")

    if user.id not in ultra_users:
        return await msg.edit(f"""<i><b>Invalid!</b></i>
"""
        )
    try:
        await db.remove_from_vars(client.me.id, "AKSES", user.id)
        await db.rem_expired_date(user_id)
        await msg.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>ID:</b> <code>{user.id}</code>
 <b>Status:</b> tidak aktif</i>
"""
        )
        for semua in DEVS:
            await bot.send_message(
                semua,
                f"<i><b>ID-Seller:</b> <code>{message.from_user.id}</code>\n<b>ID-Customer:</b> <code>{user.id}</code>\n<b>Status:</b> tidak aktif</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                            f"{message.from_user.first_name} {message.from_user.last_name or ''}",
                            url=f"tg://openmessage?user_id={message.from_user.id}",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                f"{user.first_name} {user.last_name or ''}",     url=f"tg://openmessage?user_id={user.id}"
                            ),
                        ],
                    ]
                ),
            )
    except Exception as error:
        return await msg.edit(error)


@USU.BOT("akses")
@USU.SELLER
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    replied = message.reply_to_message
    usu = message.command

    try:
        if replied:
            user_id = replied.from_user.id
            if len(usu) > 1 and usu[1].isdigit():
                get_bulan = int(usu[1])
            else:
                get_bulan = 1
        elif len(usu) > 1:
            if usu[1].isdigit():
                user_id = int(usu[1])
            else:
                try:
                    user_id = (await client.resolve_peer(usu[1])).user_id
                except Exception as error:
                    return await msg.edit(error)
            if len(usu) > 2 and usu[-1].isdigit():
                get_bulan = int(usu[-1])
            else:
                get_bulan = 1
        else:
            return await msg.edit(f"<i><b>{message.text} user_id/username - bulan</b></i>")
    except Exception as error:
        return await msg.edit(error)

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    ultra_users = await db.get_list_from_vars(client.me.id, "AKSES")

    if user.id in ultra_users or user.id in ubot._ubot:
        return await msg.edit(f"""<i><b>Sudah mempunyai Userbot aktif!</b></i>
"""
        )
    try:
        now = datetime.now(pytz.timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await db.set_expired_date(user_id, expired)
        await db.add_to_vars(client.me.id, "AKSES", user.id)
        await msg.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>ID:</b> <code>{user.id}</code>
 <b>Expired:</b> {get_bulan} Month!
 <b>Status:</b> aktif
 <b>Silahkan pencet [Install Userbot](https://t.me/{bot.me.username}?start=true)</b></i>
"""
        )
        for semua in DEVS:
            await bot.send_message(
                semua,
                f"<i><b>ID-Seller:</b> <code>{message.from_user.id}</code>\n<b>ID-Customer:</b> <code>{user.id}</code>\n<b>Status:</b> aktif {get_bulan} bulan</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                            f"{message.from_user.first_name} {message.from_user.last_name or ''}",
                            url=f"tg://openmessage?user_id={message.from_user.id}",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                f"{user.first_name} {user.last_name or ''}",     url=f"tg://openmessage?user_id={user.id}"
                            ),
                        ],
                    ]
                ),
            )
    except Exception as error:
        return await msg.edit(error)



@USU.BOT("getakses")
@USU.SELLER
async def _(client, message):
    Sh = await eor(message, f"<i><b>Processing...</b></i>")
    akses = await db.get_list_from_vars(client.me.id, "AKSES")

    if not akses:
        return await Sh.edit(f"<b><i>Empty!</i></b>")

    akses_list = []
    for user_id in akses:
        try:
            user = await client.get_users(int(user_id))
            akses_list.append(
                f"<b>[{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></b>"
            )
        except:
            continue

    if akses_list:
        response = (
            "<i><b>Daftar akses:</b>\n\n"
            + "\n".join(akses_list)
            + f"\n\n<b>Total akses:</b> <code>{len(akses_list)}</code></i>"
        )
        return await Sh.edit(response)

@USU.BOT("saldo")
@USU.DEVS
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    replied = message.reply_to_message
    usu = message.command

    try:
        if replied:
            user_id = replied.from_user.id
            if len(usu) > 1 and usu[1].isdigit():
                query = int(usu[1])
            else:
                query = int(HARGA_USERBOT)
        elif len(usu) > 1:
            if usu[1].isdigit():
                user_id = int(usu[1])
            else:
                try:
                    user_id = (await client.resolve_peer(usu[1])).user_id
                except Exception as error:
                    return await msg.edit(error)
            if len(usu) > 2 and usu[-1].isdigit():
                query = int(usu[-1])
            else:
                query = int(HARGA_USERBOT)
        else:
            return await msg.edit(f"<i><b>{message.text} user_id/username - jumlah_saldo</b></i>")
    except Exception as error:
        return await msg.edit(error)

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    vars = await db.get_vars(user.id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{query:,}".replace(",", ".")
    tambah = int(saldo) + int(query)
    topup_id = f"{user.id}{int(datetime.now().timestamp())}"

    try:
        await db.set_vars(user.id, "SALDO", tambah)
        await msg.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>ID:</b> <code>{user.id}</code>
 <b>Saldo +</b> Rp {teks}
 <b>ID Transaksi:</b> {topup_id}</i>
"""
        )
        for semua in DEVS:
            await bot.send_message(
                semua,
                f"<i><b>ID-Seller:</b> <code>{message.from_user.id}</code>\n<b>Name:</b> {user.mention}\n<b>ID:</b> <code>{user.id}</code>\n<b>Saldo +</b> Rp {teks}\n<b>ID Transaksi:</b> {topup_id}</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                            f"{message.from_user.first_name} {message.from_user.last_name or ''}",
                            url=f"tg://openmessage?user_id={message.from_user.id}",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                f"{user.first_name} {user.last_name or ''}",     url=f"tg://openmessage?user_id={user.id}"
                            ),
                        ],
                    ]
                ),
            )
    except Exception as error:
        return await msg.edit(error)


@USU.BOT("delsaldo")
@USU.DEVS
async def _(client, message):
    msg = await eor(message, f"<i><b>Processing...</b></i>")
    replied = message.reply_to_message
    usu = message.command

    try:
        if replied:
            user_id = replied.from_user.id
            if len(usu) > 1 and usu[1].isdigit():
                query = int(usu[1])
            else:
                query = int(HARGA_USERBOT)
        elif len(usu) > 1:
            if usu[1].isdigit():
                user_id = int(usu[1])
            else:
                try:
                    user_id = (await client.resolve_peer(usu[1])).user_id
                except Exception as error:
                    return await msg.edit(error)
            if len(usu) > 2 and usu[-1].isdigit():
                query = int(usu[-1])
            else:
                query = int(HARGA_USERBOT)
        else:
            return await msg.edit(f"<i><b>{message.text} user_id/username - jumlah_saldo</b></i>")
    except Exception as error:
        return await msg.edit(error)

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    vars = await db.get_vars(user.id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{query:,}".replace(",", ".")
    kurang = int(saldo) - int(query) if int(saldo) >= int(query) else 0
    topup_id = f"{user.id}{int(datetime.now().timestamp())}"

    try:      
        await db.set_vars(user.id, "SALDO", kurang)
        await msg.edit(f"""<i><b>Information!</b>
 <b>Name:</b> {user.mention}
 <b>ID:</b> <code>{user.id}</code>
 <b>Saldo -</b> Rp {teks}</i>
"""
        )
        for semua in DEVS:
            await bot.send_message(
                semua,
                f"<i><b>ID-Seller:</b> <code>{message.from_user.id}</code>\n<b>Name:</b> {user.mention}\n<b>ID:</b> <code>{user.id}</code>\n<b>Saldo -</b> Rp {teks}</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                            f"{message.from_user.first_name} {message.from_user.last_name or ''}",
                            url=f"tg://openmessage?user_id={message.from_user.id}",
                            ),
                        ],
                        [
                            InlineKeyboardButton(
                                f"{user.first_name} {user.last_name or ''}",     url=f"tg://openmessage?user_id={user.id}"
                            ),
                        ],
                    ]
                ),
            )
    except Exception as error:
        return await msg.edit(error)

