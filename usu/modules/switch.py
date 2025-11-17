from usu import *



@USU.UBOT("emoji")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(client.me.id, "switch")
    try:
        msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")

        if len(message.command) < 2:
            return await msg.edit(f"<i><b>{ggl}{message.command[0][0:]} [query] [value]</b></i>")

        query_mapping = {
          "pong": "EMOJI_PING",
          "client": "EMOJI_MENTION",
          "proses": "EMOJI_PROSES",
          "gcast": "EMOJI_BROADCAST",
          "sukses": "EMOJI_SUKSES",
          "gagal": "EMOJI_GAGAL",
          "catatan": "EMOJI_PUTARAN",
          "menunggu": "EMOJI_MENUNGGU",
          "alive": "EMOJI_UPTIME",
        }

        if len(message.command) == 2:
            query = {"on": True, "off": False}
            command = message.command[1].lower()

            if command not in query:
                return await msg.edit(f"<i><b>{ggl}{message.command[0][0:]} [on/off]!</b></i>")

            value = query[command]

            await db.set_vars(client.me.id, "switch", value)
            return await msg.edit(
                f"<i><b>{sks}Emoji {value}</b></i>"
            )

        command, mapping, value = message.command[:3]

        if mapping.lower() in query_mapping:
            if not vars:
                return await msg.edit(f"<i><b>{ggl}Silahkan aktifkan mode emojinya!\n{message.command[0][0:]} [on/off]</b></i>")
            if len(message.command) < 3:
                return await msg.edit(f"<i><b>{ggl}{message.command[0][0:]} [query] [value]</b></i>")
            query_var = query_mapping[mapping.lower()]
            emoji_id = None
            hasil = None
            if message.entities:
                for entity in message.entities:
                    if entity.custom_emoji_id:
                        emoji_id = entity.custom_emoji_id
                        hasil = f"<emoji id={emoji_id}>{value}</emoji>"
                        break
            if value.lower() == "none":
                await db.set_vars(client.me.id, query_var, False)
                return await msg.edit(
                    f"<i><b>{sks}Emoji berhasil di setting ke default!</b></i>"
                )
            elif emoji_id:
                await db.set_vars(client.me.id, query_var, emoji_id)
                return await msg.edit(
                    f"<i><b>{sks}Emoji {mapping} berhasil di setting ke {hasil}!</b></i>"
                )
            else:
                return await msg.edit(f"<i><b>{ggl}Emoji premium not found!</b></i>")
        else:
            return await msg.edit(f"<i><b>{ggl}Query tidak di temukan!</b></i>")

    except Exception as error:
        await msg.edit(str(error))


@USU.UBOT("text")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    try:
        msg = await message.reply(f"<i><b>{prs}Processing...</b></i>")

        mapping_query = {
          "pong": "ping",
          "client": "mention",
          "proses": "proses",
          "gcast": "gcast",
          "alive": "uptime",
        }

        args = message.text.split(None, 2)
        if len(args) >= 3:
            command, new_message = args[1], args[2]
            if command in mapping_query:
                query = mapping_query[command]
                if new_message.lower() == "none":
                    await db.set_vars(client.me.id, query, False)
                    await msg.edit(f"<b>{sks}Berhasil mengubah text {command} Ke : Default</b>")
                else:
                    await db.set_vars(client.me.id, query, new_message)
                    await msg.edit(f"<b>{sks}Text berhasil di settings ke : {new_message}</b>")
            else:
                await msg.edit(f"<i><b>{ggl}{message.command[0][0:]} [query] [text]</b></i>")
        else:
            await msg.edit(f"<i><b>{ggl}{message.command[0][0:]} [query] [text]</b></i>")
    except Exception as e:
        await msg.edit(e)


@USU.UBOT("inline")
async def _(client, message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    vars = await db.get_vars(client.me.id, "inline")
    if len(message.command) < 2:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>`"
        )

    query = {"on": True, "off": False}
    command = message.command[1].lower()

    if command not in query:
        return await message.reply(
            f"<i>{ggl}<code>{message.text.split()[0]}</code> <b>[on/off]</b></i>"
        )

    if command == "on":
        if not vars:
            await db.set_vars(client.me.id, "inline", query[command])
            return await message.reply(f"<i><b>{sks}Inline mode on!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Inline mode sudah on sebelumnya!</b></i>")
    else:
        if vars:
            await db.set_vars(client.me.id, "inline", query[command])
            return await message.reply(f"<i><b>{sks}Inline mode off!</b></i>")
        else:
            return await message.reply(f"<i><b>{ggl}Inline mode sudah off sebelumnya!</b></i>")