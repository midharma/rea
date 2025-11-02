import wget

from gc import get_objects

from pyrogram.types import (InlineKeyboardButton, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent)
from usu.core.helpers.tools import catbox

from usu import *


FLOOD = {}
MSG_ID = {}
PM_TEXT = """<i><b>🙋🏻‍♂️ Halo {mention}!

Saya adalah PM-Security akun ini,
Jangan spam! silahkan tunggu majikan saya online!</b></i>
"""


PMPERMIT = """Command for <b>PM-Security</b>

<b>Type</b>
 <code>|pic |text |limit</code>
 
<b>Settings PM-Security</b>
 <i>mengatur configuration pada PM-Security</i>
    <code>{0}setpm</code> [type] [text/reply/none]
 <i>mengaktifkan atau menonaktifkan PM-Security</i>
    <code>{0}pm</code> [on/off]"""


OK = """Command for <b>Approve</b>

<b>Approve</b>
 <i>menerima seseorang untuk pm anda</i>
    <code>{0}ok</code>"""

NO = """Command for <b>Disapprove</b>

<b>Disapprove</b>
 <i>menolak seseorang untuk pm anda</i>
    <code>{0}no</code>"""

FORMAT_PM = """
Command for <b>Format PM</b>

<b>Example:</b>
<code>{0}setpm text</code> isi_text ~> button_text:button_link"""

__UTAMA__ = "PM-Security"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Approve", "Set-PM", "Disapprove", "Format PM"

__HASIL__ = OK, PMPERMIT, NO, FORMAT_PM



@USU.NO_CMD("PMPERMIT", ubot)
async def _(client, message):
    sks = await EMO.SUKSES(client)
    user = message.from_user
    pm_on = await db.get_vars(client.me.id, "PMPERMIT")
    if user.id in DEVS:
        return
    if pm_on:
        if client.me.id not in MSG_ID:
            MSG_ID[client.me.id] = {}
        if user.id not in MSG_ID[client.me.id]:
            MSG_ID[client.me.id][user.id] = []
        if client.me.id in MSG_ID and user.id in MSG_ID[client.me.id]:
            await delete_old_message(client, message, MSG_ID[client.me.id][user.id])
        check = await db.get_pm_id(client.me.id)
        if user.id not in check:
            if user.id in FLOOD:
                FLOOD[user.id] += 1
            else:
                FLOOD[user.id] = 1
            pm_limit = await db.get_vars(client.me.id, "PM_LIMIT") or "5"
            if FLOOD[user.id] > int(pm_limit):
                del FLOOD[user.id]
                await message.reply(
                    f"<i><b>{sks}Maaf anda saya blokir!</i></b>"
                )
                return await client.block_user(user.id)
            pm_msg = await db.get_vars(client.me.id, "PM_TEXT") or PM_TEXT
            x = await client.get_inline_bot_results(
                bot.me.username, f"pm_pr|{client.me.id}|{FLOOD[user.id]}|{id(message)}"
            )
            msg = await client.send_inline_bot_result(
                message.chat.id,
                x.query_id,
                x.results[0].id,
                reply_to_message_id=message.id,
            )

            MSG_ID[client.me.id][user.id].append(int(msg.updates[0].id))



@USU.UBOT("setpm")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    query = {"limit": "PM_LIMIT", "text": "PM_TEXT", "pic": "PM_PIC"}
    
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[query] [value]</b><i>"
        )
    
    query_str = message.text.split(None, 2)[1].lower()
    if query_str not in query:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[type] [value]</b><i>"
        )
    
    value = query[query_str]
    
    if len(message.command) > 2:
        value_str = message.text.split(None, 2)[2]
        if not value_str:
            return await message.reply(
                f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[query] [value]</b><i>"
            )
        if query_str == "limit":
            try:
                int(value_str)
            except ValueError:
                return await message.reply(
                    f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[limit] [angka]</b><i>"
                )
        if value_str.lower() == "none":
            value_str = False 
    elif len(message.command) == 2 and message.reply_to_message:
        value_str = message.reply_to_message
        if value_str.photo or value_str.video:
            value_str = await catbox(message)
        elif value_str.text:
            value_str = f"""{value_str.text}"""
        else:
            return await message.reply(
                f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[pic] [reply_photo]</b><i>"
            )
    else:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[query] [value]</b><i>"
        )
    
    await db.set_vars(client.me.id, value, value_str)
    return await message.reply(
        f"<i><b>{sks}Success settings!</b></i>"
    )


@USU.UBOT("pm")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) < 2:
        return await message.reply(
            f"<i><code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    toggle_options = {"off": False, "on": True}
    toggle_option = message.command[1].lower()

    if toggle_option not in toggle_options:
        return await message.reply(f"<i><b>{ggl}Invalid!</b></i>")

    value = toggle_options[toggle_option]
    text = "on" if value else "off"

    await db.set_vars(client.me.id, "PMPERMIT", value)
    await message.reply(f"<i><b>{sks}PM-Permit {text}</b></i>")


@USU.INLINE("pm_pr")
async def _(client, inline_query):
    get_id = inline_query.query.split("|", 3)
    m = [obj for obj in get_objects() if id(obj) == int(get_id[3])][0]
    user_id = int(get_id[1])
    c = ubot._ubot[user_id]
    pm_msg = await db.get_vars(user_id, "PM_TEXT") or PM_TEXT
    pm_limit = await db.get_vars(user_id, "PM_LIMIT") or 5
    pm_pic = await db.get_vars(user_id, "PM_PIC")
    rpk = f"[{m.from_user.first_name} {m.from_user.last_name or ''}](tg://user?id={m.from_user.id})"
    peringatan = f"{int(get_id[2])} / {pm_limit}"
    buttons, text = await pmpermit_button(pm_msg, peringatan)
    if pm_pic:
        photo_video = InlineQueryResultVideo if pm_pic.endswith(".mp4") else InlineQueryResultPhoto
        photo_video_url = {"video_url": pm_pic, "thumb_url": pm_pic} if pm_pic.endswith(".mp4") else {"photo_url": pm_pic}
        results = [
            photo_video(
                **photo_video_url,
                title="Dapatkan tombol!",
                caption=text.format(mention=rpk),
                reply_markup=buttons,
            )
        ]
    else:
        results = [
            (
                InlineQueryResultArticle(
                    title="Dapatkan tombol!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text.format(mention=rpk)),
                )
            )
        ]
    await inline_query.answer(results=results)

@USU.CALLBACK("^pm_warn")
async def limit(client, callback_query):
    return await callback_query.answer(f"Mohon jangan spam!", True)



async def pmpermit_button(m, peringatan):
    keyboard = []
    keyboard.append([InlineKeyboardButton(f"Peringatan {peringatan} hati-hati!", callback_data="pm_warn")])

    if "~>" in m:
        usu_buttons = []
        for X in m.split("~>", 1)[1].split():
            X_parts = X.split(":", 1)
            usu_buttons.append(InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1]))
            if len(usu_buttons) == 2:
                keyboard.append(usu_buttons)
                usu_buttons = []
        if usu_buttons:
            keyboard.append(usu_buttons)

    buttons = InlineKeyboardMarkup(keyboard)
    text = m.split("~>", 1)[0] if "~>" in m else m
    return buttons, text


@USU.UBOT("ok|terima")
@USU.PRIVATE
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    vars = await db.get_pm_id(client.me.id)
    if user.id not in vars:
        await db.add_pm_id(client.me.id, user.id)
        usu = await message.reply(f"<i><b>{sks}Baiklah, {rpk} telah diterima!</b></i>")
        if client.me.id in MSG_ID and user.id in MSG_ID[client.me.id]:
            await delete_old_message(client, message, MSG_ID[client.me.id][user.id])
    else:
        usu = await message.reply(f"<b><i>{ggl}Maaf {rpk} sudah diterima sebelumnya!</i></b>")
    await asyncio.sleep(5)
    await message.delete()
    await usu.delete()


@USU.UBOT("no|tolak")
@USU.PRIVATE
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    user = message.chat
    rpk = f"[{user.first_name} {user.last_name or ''}](tg://user?id={user.id})"
    vars = await db.get_pm_id(client.me.id)
    if user.id not in vars:
        await message.reply(f"<i><b>{sks}Maaf ⁣{rpk} anda telah diblokir!</b></i>")
        return await client.block_user(user.id)
    else:
        await db.remove_pm_id(client.me.id, user.id)
        return await message.reply(
            f"<i><b>{sks}Maaf {rpk} anda telah ditolak untuk menghubungi saya!</b></i>"
        )


async def delete_old_message(client, message, msg_id):
    try:
        for target in msg_id:
            await client.delete_messages(message.chat.id, target)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        for target in msg_id:
            await client.delete_messages(message.chat.id, target)
    except:
        for target in msg_id:
            await client.delete_messages(message.chat.id, target)


