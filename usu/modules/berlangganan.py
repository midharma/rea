from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from usu import *
import os
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pytz import timezone


langganan_info = {}

@USU.CALLBACK("beli")
async def beli_langganan(client, callback_query):
    user_id = callback_query.from_user.id
    langganan_info[user_id] = 1
    return await callback_query.edit_message_text(
        f"<i><b>Silakan pilih jumlah masa aktif [Userbot]({QRIS}) yang anda inginkan:</b>\n1 Bulan - Rp {HARGA_USERBOT}.000",
        reply_markup=InlineKeyboardMarkup(BTN.PAY(1))
    )

@USU.CALLBACK("kiri_")
async def prev_bulan(client, callback_query):
    user_id = callback_query.from_user.id
    try:
        bulan_saat_ini = int(callback_query.data.split("_")[1])
        if bulan_saat_ini > 1:
            langganan_info[user_id] = bulan_saat_ini - 1
            jumlah_bulan = langganan_info[user_id]
            total_harga = jumlah_bulan * HARGA_USERBOT
            await callback_query.edit_message_text(
                f"<i><b>Silakan pilih jumlah masa aktif [Userbot]({QRIS}) yang anda inginkan:</b>\n{jumlah_bulan} Bulan - Rp {total_harga}.000",
                reply_markup=InlineKeyboardMarkup(BTN.PAY(jumlah_bulan))
            )
        else:
            await callback_query.answer("Ini adalah bulan pertama.", show_alert=True)
    except Exception as e:
        return print(e)


@USU.CALLBACK("kanan_")
async def next_bulan(client, callback_query):
    user_id = callback_query.from_user.id
    try:
        bulan_saat_ini = int(callback_query.data.split("_")[1])
        langganan_info[user_id] = bulan_saat_ini + 1
        jumlah_bulan = langganan_info[user_id]
        total_harga = jumlah_bulan * HARGA_USERBOT
        await callback_query.edit_message_text(
            f"<i><b>Silakan pilih jumlah masa aktif [Userbot]({QRIS}) yang anda inginkan:</b>\n{jumlah_bulan} Bulan - Rp {total_harga}.000",
            reply_markup=InlineKeyboardMarkup(BTN.PAY(jumlah_bulan))
        )
    except Exception as e:
        return print(e)

@USU.CALLBACK("tambahkan")
async def tambah_akses(client, callback_query):
    data = callback_query.data.split()
    bulan = int(data[1])
    user_id = int(data[2])
    btn = [[InlineKeyboardButton("Install Userbot", callback_data="buat")]]
    if callback_query.from_user.id not in DEVS:
        return await ("Tombol ini untuk Owner!", True)
    if user_id not in await db.get_list_from_vars(client.me.id, "AKSES"):
        try:
            user = await client.get_users(user_id)
        except Exception as e:
            return print(e)
        now = datetime.now(pytz.timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(bulan))
        await db.set_expired_date(user_id, expired)
        await db.add_to_vars(client.me.id, "AKSES", user_id)
        await client.send_message(user_id, f"<i><b>Pembelian [Userbot]({PHOTO}) anda sudah dikonfirmasi oleh {USERNAME}!\nName:</b> {user.mention}\n<b>ID:</b> {user.id}\n<b>Masa aktif:</b> {bulan} bulan\n\n<b>Silahkan install Userbot anda!</b></i>", reply_markup=InlineKeyboardMarkup(btn))
        return await callback_query.answer("Berhasil diakses!", True)
    else:
        return await callback_query.answer("Sudah diakses sebelumnya!", True)


@USU.CALLBACK("bayar_")
async def proses_bayar(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in langganan_info:
        jumlah_bulan = langganan_info[user_id]
        total_harga = jumlah_bulan * HARGA_USERBOT
        btns = [[InlineKeyboardButton(f"Akses {jumlah_bulan} bulan", callback_data=f"tambahkan {jumlah_bulan} {user_id}")], [InlineKeyboardButton(f"Kirim Pesan", callback_data=f"jawab_pesan {user_id}")]]
        batal = [[InlineKeyboardButton("Kembali", callback_data=f"beli")]]
        try:
            anu = await client.ask(
                user_id,
                f"<i><b>Silakan scan [QRIS]({QRIS}) di dibawah untuk membayar Rp {total_harga}.000 ({jumlah_bulan} bulan)!\n\nCatatan:</b> wajib kirim bukti screenshot!</i>", reply_markup=InlineKeyboardMarkup(batal), timeout=300
            )
            if anu.photo:
                for asu in DEVS:
                    try:
                        await client.send_photo(asu, caption=f"<i><b>Information!</b>\n<b>Name:</b> {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}\n<b>ID:</b> {user_id}</i>", photo=anu.photo.file_id, reply_markup=InlineKeyboardMarkup(btns))
                    except Exception as e:
                        del langganan_info[user_id]
                        return print(e)
                await client.send_message(user_id, f"<b><i>Silahkan tunggu dalam 1x24 jam, {USERNAME} akan secepatnya mengkonfirmasi pembelian Userbot anda!</i></b>")
            else:
                await client.send_message(user_id, f"<b><i>Tidak ada bukti transfer, silahkan coba /start kembali!</i></b>")
        except asyncio.TimeoutError:
            del langganan_info[user_id]
            return await client.send_message(user_id, f"<b><i>Pembelian dibatalkan otomatis!</b></i>")

        del langganan_info[user_id]
        return
    else:
        await callback_query.answer("Terjadi kesalahan, silakan coba lagi.", show_alert=True)