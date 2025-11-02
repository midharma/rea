import os
from gc import get_objects

import gtts
from gpytranslate import Translator

from usu import *





@USU.UBOT("tts")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    TM = await message.reply(f"<i><b>{prs}Processing...</b></i>")
    if message.reply_to_message:
        language = client._translate[client.me.id]
        words_to_say = message.reply_to_message.text or message.reply_to_message.caption
    else:
        if len(message.command) < 2:
            return await TM.edit(f"<i><b>{ggl}<code>{message.text}</code> [text/text]</i></b>")
        else:
            language = client._translate[client.me.id]
            words_to_say = message.text.split(None, 1)[1]
    speech = gtts.gTTS(words_to_say, lang=language)
    speech.save("text_to_speech.oog")
    rep = message.reply_to_message or message
    try:
        await client.send_voice(
            chat_id=message.chat.id,
            voice="text_to_speech.oog",
            reply_to_message_id=rep.id,
        )
        await TM.delete()
    except Exception as error:
        await TM.edit(error)
    try:
        os.remove("text_to_speech.oog")
    except FileNotFoundError:
        pass


@USU.UBOT("tr")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    trl = Translator()
    if not message.reply_to_message:
        return await message.reply("<i><b>{ggl}No message to translate!</b></i>")

    text = message.reply_to_message.text or message.reply_to_message.caption

    if not text:
        return await message.reply(f"<i><b>{ggl}No text found in the message.</b></i>")

    input_str = message.text.split(None, 1)[1] if len(message.command) > 1 else None
    target = input_str or "id"

    try:
        tekstr = await trl(text, targetlang=target)
        detected_lang = await trl.detect(text)
    except ValueError as err:
        return await message.reply("<i><b>{ggl}Error occurred during translation!</b></i>")

    reply_text = (
        f"<b>{broad}Translated to:</b> <code>{target}\n{tekstr.text}</code>\n\n"
        f"<b>{sks}Detected Language:</b> <code>{detected_lang}</code>"
    )

    await message.reply(f"<i>{reply_text}</i>")
