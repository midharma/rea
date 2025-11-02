from usu import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import enums
from pyrogram.errors import FloodWait

async def format_button(m):
    keyboard = []
    text = m.split("|")[0].strip() if "|" in m else m.strip()
    buttons = None
    if "|" in m:
        usu_buttons = []
        for X in m.split("|")[1:]:
            if X.strip():
                X_parts = X.split(" - ", 1)
                if len(X_parts) == 2:
                    usu_buttons.append(InlineKeyboardButton(X_parts[0].strip(), url=X_parts[1].strip()))
                if len(usu_buttons) == 2:
                    keyboard.append(usu_buttons)
                    usu_buttons = []
        if usu_buttons:
           keyboard.append(usu_buttons)
        if keyboard:
           buttons = InlineKeyboardMarkup(keyboard)
    return buttons, text


@USU.NO_CMD("WELCOME", bot)
async def member_baru(c, m):
    group = await db.get_list_from_vars(bot.me.id, "group")
    pesan = await MSG.MEMBER()
    tombol = BTN.MEMBER()
    vars = await db.get_vars(m.chat.id, "WELCOME")
    sudo = await db.get_list_from_vars(bot.me.id, "SUDO")
    asw = None
    try:
        asw = await c.get_chat(m.chat.id)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        asw = await c.get_chat(m.chat.id)
    except Exception as e:
        pass
    if asw:
        haw = f"[{m.chat.title}]({asw.invite_link})" if asw.invite_link else f"[{m.chat.title}](https://t.me/{asw.username})" if asw.username else m.chat.title
        hasil = f"""<i><b>Informasi!</b>
<b>Judul Obrolan:</b> {haw}
<b>ID Obrolan:</b> {m.chat.id}
<b>Status:</b> ditambahkan</i>"""
        user = [[InlineKeyboardButton(f"Ditambahkan Oleh", url=f"tg://openmessage?user_id={m.from_user.id}")]]
        for target in m.new_chat_members:
            if target.id == bot.me.id:
                if m.chat.id not in group:
                    await db.add_to_vars(bot.me.id, "group", m.chat.id)
                    await bot.send_message(m.chat.id, pesan, reply_markup=InlineKeyboardMarkup(tombol))
                if LOGS_CHAT:
                    return await bot.send_message(LOGS_CHAT, hasil, reply_markup=InlineKeyboardMarkup(user))
                return
            elif target.id in DEVS:
                return await bot.send_message(m.chat.id, f"<b><i>Pemilik bot ini {target.mention} telah bergabung di chat anda!</i></b>")
            elif target.id in sudo:
                return await bot.send_message(m.chat.id, f"<b><i>Pengguna sudo bot ini {target.mention} telah bergabung di chat anda!</i></b>")
        if vars:
            for user in m.new_chat_members:
                if not user.is_bot:
                    format = {
                        "{mention}": f"{user.mention}",
                        "{user_id}": f"{user.id}",
                        "{username}": f"{user.username or ''}",
                        "{chat_id}": f"{m.chat.id}",
                        "{chat_title}": f"{m.chat.title}",
                        "{first_name}": f"{user.first_name}",
                        "{last_name}": f"{user.last_name or ''}",
                    }
                    teks = vars.get("text")
                    if teks:
                        btn, teks = await format_button(teks)
                        for key, value in format.items():
                            if key in teks:
                                teks = teks.replace(key, value)
                    file = vars.get("file")
                    if file:
                        if teks:
                            try:
                                if btn is not None:
                                    usu = await bot.send_cached_media(m.chat.id, file, caption=teks, reply_markup=btn)
                                else:
                                    usu = await bot.send_cached_media(m.chat.id, file, caption=teks)
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                if btn is not None:
                                    usu = await bot.send_cached_media(m.chat.id, file, caption=teks, reply_markup=btn)
                                else:
                                    usu = await bot.send_cached_media(m.chat.id, file, caption=teks)
                            except Exception as e:
                                pass
                        else:
                            try:
                                usu = await bot.send_cached_media(m.chat.id, file)
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                usu = await bot.send_cached_media(m.chat.id, file)
                            except Exception as e:
                                pass
                    elif teks:
                        try:
                            if btn is not None:
                                usu = await bot.send_message(m.chat.id, teks, reply_markup=btn)
                            else:
                                usu = await bot.send_message(m.chat.id, teks)
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            if btn is not None:
                                usu = await bot.send_message(m.chat.id, teks, reply_markup=btn)
                            else:
                                usu = await bot.send_message(m.chat.id, teks)
                        except Exception as e:
                            pass
                    if usu:
                        await asyncio.sleep(60)
                        await usu.delete()


@USU.NO_CMD("LEFT", bot)
async def member_keluar(c, m):
    group = await db.get_list_from_vars(bot.me.id, "group")
    anjay = await db.get_vars(m.chat.id, "GOODBYE")
    haw = m.chat.title
    hasil = f"""<i><b>Informasi!</b>
<b>Judul Obrolan:</b> {haw}
<b>ID Obrolan:</b> {m.chat.id}
<b>Status:</b> dikeluarkan</i>"""
    user = [[InlineKeyboardButton(f"Dikeluarkan Oleh", url=f"tg://openmessage?user_id={m.from_user.id}")]]
    if m.left_chat_member and m.left_chat_member.id == bot.me.id:
        if m.chat.id in group and m.chat.type != enums.ChatType.CHANNEL:
            await db.remove_from_vars(bot.me.id, "group", m.chat.id)
        if LOGS_CHAT:
            await bot.send_message(LOGS_CHAT, hasil, reply_markup=InlineKeyboardMarkup(user))

    if anjay:
        user = m.left_chat_member
        if user and user.id:
            format = {
                "{mention}": f"{user.mention}",
                "{user_id}": f"{user.id}",
                "{username}": f"{user.username or ''}",
                "{chat_id}": f"{m.chat.id}",
                "{chat_title}": f"{m.chat.title}",
                "{first_name}": f"{user.first_name}",
                "{last_name}": f"{user.last_name or ''}",
                }
            teks = anjay.get("text")
            if teks:
                btn, teks = await format_button(teks)
                for key, value in format.items():
                    if key in teks:
                        teks = teks.replace(key, value)
            file = anjay.get("file")
            if file:
                try:
                    if btn is not None:
                        usu = await bot.send_cached_media(m.chat.id, file, caption=teks, reply_markup=btn)
                    else:
                        usu = await bot.send_cached_media(m.chat.id, file, caption=teks)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    if btn is not None:
                        usu = await bot.send_cached_media(m.chat.id, file, caption=teks, reply_markup=btn)
                    else:
                        usu = await bot.send_cached_media(m.chat.id, file, caption=teks)
                except Exception as e:
                    pass
            elif teks:
                try:
                    if btn is not None:
                        usu = await bot.send_message(m.chat.id, teks, reply_markup=btn)
                    else:
                        usu = await bot.send_message(m.chat.id, teks)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    if btn is not None:
                        usu = await bot.send_message(m.chat.id, teks, reply_markup=btn)
                    else:
                        usu = await bot.send_message(m.chat.id, teks)
                except Exception as e:
                    pass
            if usu:
                await asyncio.sleep(60)
                await usu.delete()

