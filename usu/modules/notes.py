from pyrogram.types import *

from usu import *



DELETE = """Command for <b>Delete Note</b>

<b>Delete Note</b>
 <i>menghapus catatan yang di simpan</i>
    <code>{0}delnote</code> [titel note]
 <i>menghapus callback yang di simpan</i
    <code>{0}delcb</code> [title cb]"""

LIST = """Command for <b>List Note</b>

<b>List Note</b>
 <i>melihat daftar catatan yang di simpan</i>
    <code>{0}listnote</code> [title note]
 <i>melihat daftar callback yang di simpan</i>
    <code>{0}listcb</code> [title cb]"""


GET = """Command for <b>Get Note</b>

<b>Get Note</b>
 <i>mendapatkan catatan yang di simpan</i>
    <code>{0}get</code> [title note/cb]"""


SAVE = """Command for <b>Add Note</b>

<b>Add Note</b>
 <i>menyimpan sebuah catatan</i>
    <code>{0}addnote</code> [title]
 <i>menyiman callback catatan</i>
   <code>{0}addcb</code> [title]"""


FORMAT = """Command for <b>Format Notes</b>

<b>Example notes button</b>
 <code>{0}addnote</code> text bebas | nama button - link/callback |"""


__UTAMA__ = "Notes"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Format Note", "Delete Note", "List Note", "Get Note","Add Note"

__HASIL__ = FORMAT, DELETE, LIST, GET, SAVE


@USU.UBOT("addnote|addcb")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    args = get_arg(message)
    reply = message.reply_to_message
    query = "notes_cb" if message.command[0] == "addcb" else "notes"

    if not args or not reply:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[name] [text/reply]</b></i>"
        )

    vars = await db.get_vars(client.me.id, args, query)

    if vars:
        return await message.reply(f"<i><b>{ggl}Notes {args} already available!</b></i>")

    value = None
    type_mapping = {
        "text": reply.text,
        "photo": reply.photo,
        "voice": reply.voice,
        "audio": reply.audio,
        "video": reply.video,
        "animation": reply.animation,
        "sticker": reply.sticker,
    }

    for media_type, media in type_mapping.items():
        if media:
            send = await reply.copy(client.me.id)
            value = {
                "type": media_type,
                "message_id": send.id,
            }
            break

    if value:
        await db.set_vars(client.me.id, args, value, query)
        return await message.reply(
            f"<i><b>{sks}Notes <code>{args}</code> saved!</b>"
        )
    else:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[name] [text/reply]</b></i>"
        )


@USU.UBOT("delnote|delcb")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    args = get_arg(message)

    if not args:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[name]</b></i>"
        )

    query = "notes_cb" if message.command[0] == "delcb" else "notes"
    vars = await db.get_vars(client.me.id, args, query)

    if not vars:
        return await message.reply(f"<i><b>{ggl}Notes {args} not found!</b></i>")

    await db.remove_vars(client.me.id, args, query)
    await client.delete_messages(client.me.id, int(vars["message_id"]))
    return await message.reply(f"<i><b>{sks}Notes {args} deleted!</b></i>")


@USU.UBOT("get")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    msg = message.reply_to_message or message
    args = get_arg(message)

    if not args:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[name]</b></i>"
        )

    data = await db.get_vars(client.me.id, args, "notes")

    if not data:
        return await message.reply(
            f"<i><b>{ggl}Notes {args} not found!</b></i>"
        )

    m = await client.get_messages(client.me.id, int(data["message_id"]))

    if data["type"] == "text":
        if matches := re.findall(r"\| ([^|]+) - ([^|]+) \|", m.text):
            try:
                x = await client.get_inline_bot_results(
                    bot.me.username, f"get_notes {client.me.id} {args}"
                )
                return await client.send_inline_bot_result(
                    message.chat.id,
                    x.query_id,
                    x.results[0].id,
                    reply_to_message_id=msg.id,
                )
            except Exception as error:
                await message.reply(error)
        else:
            return await m.copy(message.chat.id, reply_to_message_id=msg.id)
    else:
        return await m.copy(message.chat.id, reply_to_message_id=msg.id)


@USU.UBOT("listnote|listcb")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    query = "notes_cb" if message.command[0] == "listcb" else "notes"
    vars = await db.all_vars(client.me.id, query)
    if vars:
        msg = f"<b>{broad}Notes!</b>\n\n"
        for x, data in vars.items():
            msg += f" {x} |({data['type']})\n"
        msg += f"<b>\n{sks}Total notes: {len(vars)}</b>"
    else:
        msg = f"<b>{ggl}Empty!</b>"

    return await message.reply(f"<i>{msg}</i>", quote=True)


@USU.INLINE("^get_notes")
async def _(client, inline_query):
    query = inline_query.query.split()
    data = await db.get_vars(int(query[1]), query[2], "notes")
    item = [x for x in ubot._ubot.values() if int(query[1]) == x.me.id]
    for me in item:
        m = await me.get_messages(int(me.me.id), int(data["message_id"]))
        buttons, text = create_inline_keyboard(m.text, f"{int(query[1])}_{query[2]}")
        results = [
            (
                InlineQueryResultArticle(
                    title="get notes!",
                    reply_markup=buttons,
                    input_message_content=InputTextMessageContent(text),
                )
            )
        ]
        return await inline_query.answer(results=results)


@USU.CALLBACK("_gtnote")
async def _(client, callback_query):
    _, user_id, *query = callback_query.data.split()
    data_key = "notes_cb" if bool(query) else "notes"
    query_eplit = query[0] if bool(query) else user_id.split("_")[1]
    data = await db.get_vars(int(user_id.split("_")[0]), query_eplit, data_key)
    item = [x for x in ubot._ubot.values() if int(user_id.split("_")[0]) == x.me.id]
    for me in item:
        m = await me.get_messages(int(me.me.id), int(data["message_id"]))
        buttons, text = create_inline_keyboard(
            m.text, f"{int(user_id.split('_')[0])}_{user_id.split('_')[1]}", bool(query)
        )
        return await callback_query.edit_message_text(text, reply_markup=buttons)
