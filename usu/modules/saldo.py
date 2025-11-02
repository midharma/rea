from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from usu import *
import os
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone


info_data = {}

@USU.CALLBACK("saldo")
async def saldo(c, cq):
    data = cq.data.split()
    user_id = cq.from_user.id
    if user_id in info_data:
        del info_data[user_id]
    btn = BTN.TOPUP()
    vars = await db.get_vars(user_id, "SALDO")
    saldo = vars if vars else 0
    teks = f"{saldo:,}".replace(",", ".")
    text = f"<i><b>Saldo [Userbot]({PHOTO}) anda saat ini:\n</b>Rp {teks}</i>"
    return await cq.edit_message_text(text, reply_markup=InlineKeyboardMarkup(btn))

@USU.CALLBACK("kode")
async def kode(c, cq):
    user_id = cq.from_user.id
    ref = f"REF{user_id}"
    total = await db.get_list_from_vars(user_id, "REF")
    undang = BTN.REF(bot.me.username, ref)
    text = f"<i><b>Undang pengguna baru menggunakan kode Referral bisa menambahkan saldo anda, mengundang 1 pengguna baru bisa mendapatkan saldo Rp 4.000 setiap undang nya!\n\nReferral Anda:</b>\n<code>https://t.me/{bot.me.username}?start={ref}</code>\n\n<b>Total Diundang:</b> {len(total)}</i>"
    return await cq.edit_message_text(text, reply_markup=InlineKeyboardMarkup(undang))


@USU.CALLBACK("isi")
async def isi_saldo(c, cq):
    user_id = cq.from_user.id
    batal = [[InlineKeyboardButton("Kembali", callback_data=f"saldo")]]
    try:
        anu = await c.ask(
            user_id,
            f"<i><b>Silakan ketik nominal yang anda inginkan!\nContoh:</b> 10000</i>", reply_markup=InlineKeyboardMarkup(batal), timeout=300
        )
        if anu.text.isdigit():
            teks = f"{int(anu.text):,}".replace(",", ".")
            try:
                asu = await c.ask(
                    user_id,
                    f"<i><b>Silakan scan [QRIS]({QRIS}) di dibawah sesuai Rp {teks}\n\nCatatan:</b> wajib kirim bukti screenshot!</i>", reply_markup=InlineKeyboardMarkup(batal), timeout=300
                )
                if asu.photo:
                    topup_id = f"{user_id}{int(datetime.now().timestamp())}"
                    info_data[user_id] = {"topup_id": topup_id, "saldo": anu.text}
                    for anj in DEVS:
                        try:
                            await c.send_photo(anj, caption=f"<i><b>Information!\nName:</b> {cq.from_user.first_name} {cq.from_user.last_name or ''}\n<b>ID:</b> {user_id}\n<b>Jumlah topup:</b> Rp {teks}\n<b>ID Transaksi:</b> {topup_id}</i>", photo=asu.photo.file_id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Konfirmasi Rp {teks}", callback_data=f"price {user_id}")], [InlineKeyboardButton(f"Kirim Pesan", callback_data=f"jawab_pesan {user_id}")]]))
                        except Exception as e:
                            return logger.error(e)
                    return await c.send_message(user_id, f"<i><b>Information!\nName:</b> {cq.from_user.first_name} {cq.from_user.last_name or ''}\n<b>ID Transaksi:</b> {topup_id}\n\n<b>Silahkan tunggu dalam 1x24 jam, @{USERNAME} akan secepatnya mengkonfirmasi pengisian saldo Userbot anda!</b></i>")
                else:
                    return await c.send_message(user_id, f"<b><i>Tidak ada bukti transfer, silahkan coba /start kembali!</i></b>")
            except asyncio.TimeoutError:
                del info_data[user_id]
                return await c.send_message(user_id, f"<b><i>Pembelian dibatalkan otomatis!</b></i>")
        else:
            return await c.send_message(user_id, f"<b><i>Format berupa angka, silahkan coba /start kembali!</i></b>")
    except asyncio.TimeoutError:
        del info_data[user_id]
        return await c.send_message(user_id, f"<b><i>Pembelian dibatalkan otomatis!</b></i>")


@USU.CALLBACK("price")
async def tambah_saldo(c, cq):
    data = cq.data.split()
    tx = int(data[1])
    if cq.from_user.id not in DEVS:
        return await ("Tombol ini untuk Owner!", True)
    if tx in info_data:
        idtx = info_data[tx]["topup_id"]
        saldo = info_data[tx]["saldo"]
        teks = f"{int(saldo):,}".replace(",", ".")
        try:
            user = await c.get_users(tx)
            vars_data = await db.get_vars(user.id, "TX")
            vars = await db.get_vars(user.id, "SALDO")
            current_saldo = vars if vars else 0
            topup_ids = vars_data if vars_data else []
            hasil = int(current_saldo) + int(saldo)
            await db.set_vars(user.id, "SALDO",  hasil)
            await c.send_message(user.id, f"<i><b>Pengisian saldo [Userbot]({PHOTO}) anda sudah dikonfirmasi oleh {USERNAME}!\n\nName:</b> {user.mention}\n<b>ID:</b> {user.id}\n<b>Jumlah topup:</b> Rp {teks}\n<b>ID Transaksi:</b> {idtx}</i>", reply_markup=InlineKeyboardMarkup(BTN.START()))
            await cq.answer("Berhasil dikonfirmasi!", True)
            del info_data[tx]
        except Exception as e:
            del info_data[tx]
            logger.error(e)
            return
    else:
        return await cq.answer("Sudah dikonfirmasi sebelumnya!", True)