from math import ceil

from usu.core.helpers.font_help import *

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from usu import *


tombol_utama = {}
tombol_anak = {}




async def tombol_usu():
    btn = [InlineKeyboardButton("🔙 Kembali", callback_data="menu_utama")]
    markup = InlineKeyboardMarkup([])
    row = []
    for item in tombol_utama.values():
        text = item["text"]
        data = item["callback_data"]
        row.append(InlineKeyboardButton(text=text, callback_data=data))
        if len(row) == 3:
            markup.inline_keyboard.append(row)
            row = []
    if row:
        markup.inline_keyboard.append(row)
        markup.inline_keyboard.append(btn)
    return markup


#For button anak!
LEBAR = 2
TINGGI = 4


async def tombol_anak_usu_gbt(utama, page):
    markup = InlineKeyboardMarkup([])
    tombol_anak_list = sorted(tombol_anak[utama], key=lambda x: x['text'])
    jumlah_tombol = len(tombol_anak_list)
    per_page = LEBAR * TINGGI
    max_num_pages = ceil(jumlah_tombol / per_page) if per_page > 0 else 1
    current_page = page % max_num_pages  # Gunakan current_page untuk kejelasan
    start_index = current_page * per_page
    end_index = min(start_index + per_page, jumlah_tombol)
    buttons_on_page = tombol_anak_list[start_index:end_index]

    index = 0
    for i in range(TINGGI):
        row = []
        for j in range(LEBAR):
            if index < len(buttons_on_page):
                row.append(InlineKeyboardButton(text=buttons_on_page[index]['text'], callback_data=buttons_on_page[index]['callback_data']))
                index += 1
        if row:
            markup.inline_keyboard.append(row)

    navigasi_row = []
    if max_num_pages > 1:
        prev_page = (current_page - 1 + max_num_pages) % max_num_pages
        next_page = (current_page + 1) % max_num_pages
        navigasi_row.append(InlineKeyboardButton(text="« Prev", callback_data=f"prev_{utama}_{prev_page}"))
        navigasi_row.append(InlineKeyboardButton(text=f"{current_page + 1}/{max_num_pages}", callback_data="ignore"))
        navigasi_row.append(InlineKeyboardButton(text="Next »", callback_data=f"next_{utama}_{next_page}"))
        markup.inline_keyboard.append(navigasi_row) 
        markup.inline_keyboard.append([InlineKeyboardButton(text="Kembali", callback_data=f"kembali")])
    else:
        markup.inline_keyboard.append([InlineKeyboardButton(text="Kembali", callback_data=f"kembali")])

    return markup