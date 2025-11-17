from gc import get_objects

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)

from usu import *




@USU.UBOT("msg")
async def _(client, message):
    ggl = await EMO.GAGAL(client)
    if not message.reply_to_message or len(message.command) < 2:
        return await message.reply(f"<b><i>{ggl}msg [reply - text]</i></b>")
    text = f"secret {id(message)}"
    await message.delete()
    x = await client.get_inline_bot_results(bot.me.username, text)
    for m in x.results:
        await message.reply_to_message.reply_inline_bot_result(x.query_id, m.id)


@USU.INLINE("^secret")
async def _(client, inline_query):
    m = [obj for obj in get_objects() if id(obj) == int(inline_query.query.split(None, 1)[1])][0]
    results = [
        (
            InlineQueryResultArticle(
                title="Pesan Rahasia!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Buka!",
                                callback_data=f"read {inline_query.query.split(None, 1)[1]}",
                            )
                        ],
                    ]
                ),
                input_message_content=InputTextMessageContent(
                    f"<b>Ada pesan untukmu!:</b> <a href=tg://user?id={m.reply_to_message.from_user.id}>{m.reply_to_message.from_user.first_name} {m.reply_to_message.from_user.last_name or ''}</a>"
                ),
            )
        )
    ]
    await inline_query.answer(results=results)


@USU.CALLBACK("^read")
async def _(client, cq):
    m = [obj for obj in get_objects() if id(obj) == int(cq.data.split(None, 1)[1])][0]
    anunya = [
        getattr(getattr(m, "reply_to_message", None), "from_user", None) and m.reply_to_message.from_user.id,
        getattr(getattr(m, "_client", None), "me", None) and m._client.me.id,
    ]
    if cq.from_user.id not in anunya:
        return await cq.answer(
            f"Tombol ini bukan buat anda! {cq.from_user.first_name} {cq.from_user.last_name or ''}",
            True,
        )
    await cq.answer(m.text.split(None, 1)[1], True)