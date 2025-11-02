from gc import get_objects
from usu import *
from pyrogram import Client, filters, types
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)



async def create_button(m):
    keyboard = []
    msg = []
    if "~>" not in m.text.split(None, 1)[1]:
        usu_buttons = []
        for X in m.text.split(None, 1)[1].split():
            X_parts = X.split(":", 1)
            usu_buttons.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
            msg.append(X_parts[0])
            if len(usu_buttons) == 2:
                keyboard.append(usu_buttons)
                usu_buttons = []
        if usu_buttons:
            keyboard.append(usu_buttons)
        if m.reply_to_message:
            text = m.reply_to_message.text
        else:
            text = " ".join(msg)
    else:
        usu_buttons = []
        for X in m.text.split("~>", 1)[1].split():
            X_parts = X.split(":", 1)
            usu_buttons.append(
                InlineKeyboardButton(X_parts[0].replace("_", " "), url=X_parts[1])
            )
            if len(usu_buttons) == 2:
                keyboard.append(usu_buttons)
                usu_buttons = []
        if usu_buttons:
            keyboard.append(usu_buttons)
        text = m.text.split("~>", 1)[0].split(None, 1)[1]
    buttons = InlineKeyboardMarkup(keyboard)

    return buttons, text



@USU.UBOT("button")
async def cmd_button(client, message):
    if len(message.command) < 2:
        return await message.reply(f"{message.text} text ~> button_name:link_url")
    if "~>" not in message.text:
        return await message.reply(
            f"<i><b>Please check the help button</b></i>"
        )
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"get_button {id(message)}"
        )
        msg = message.reply_to_message or message
        await client.send_inline_bot_result(
            message.chat.id, x.query_id, x.results[0].id, reply_to_message_id=msg.id
        )
    except Exception as error:
        await message.reply(error)


@USU.INLINE("^get_button")
async def inline_button(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    m = [obj for obj in get_objects() if id(obj) == get_id][0]
    buttons, text = await create_button(m)
    results = [
        (
            InlineQueryResultArticle(
                title="get button!",
                reply_markup=buttons,
                input_message_content=InputTextMessageContent(text),
            )
        )
    ]
    await inline_query.answer(results=results)