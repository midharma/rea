from usu import *



class EMO:
    async def PING(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_1 = await db.get_vars(client.me.id, "EMOJI_PING")
        emot_ping = emot_1 if emot_1 else "5202089931085718160"
        return f"<emoji id={emot_ping}>🏓</emoji>"

    async def MENTION(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_2 = await db.get_vars(client.me.id, "EMOJI_MENTION")
        emot_tion = emot_2 if emot_2 else "5424605254614262924"
        return f"<emoji id={emot_tion}>⭐️</emoji>"

    async def UPTIME(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_12 = await db.get_vars(client.me.id, "EMOJI_UPTIME")
        emot_up = emot_12 if emot_12 else "5224533828151812094"
        return f"<emoji id={emot_up}>⏰</emoji>"

    async def PROSES(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_4 = await db.get_vars(client.me.id, "EMOJI_PROSES")
        emot_prs = emot_4 if emot_4 else "5201877502003258204"
        return f"<emoji id={emot_prs}>⏳</emoji>"

    async def SUKSES(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_5 = await db.get_vars(client.me.id, "EMOJI_SUKSES")
        emot_brhsl = emot_5 if emot_5 else "5427295974315793487"
        return f"<emoji id={emot_brhsl}>✅</emoji>"

    async def GAGAL(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_6 = await db.get_vars(client.me.id, "EMOJI_GAGAL")
        emot_ggl = emot_6 if emot_6 else "5292222401067626057"
        return f"<emoji id={emot_ggl}>❌</emoji>"

    async def BROADCAST(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_7 = await db.get_vars(client.me.id, "EMOJI_BROADCAST")
        emot_gcs = emot_7 if emot_7 else "5451694459458690201"
        return f"<emoji id={emot_gcs}>📣</emoji>"

    async def MENUNGGU(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_10 = await db.get_vars(client.me.id, "EMOJI_MENUNGGU")
        emot_mng = emot_10 if emot_10 else "5285409457654737374"
        return f"<emoji id={emot_mng}>⏰</emoji>"

    async def PUTARAN(client):
        varss = await db.get_vars(client.me.id, "switch")
        if not varss:
            return ""
        emot_11 = await db.get_vars(client.me.id, "EMOJI_PUTARAN")
        emot_ptr = emot_11 if emot_11 else "5258513401784573443"
        return f"<emoji id={emot_ptr}>🌀</emoji>"


class TEXT:
    async def PING(client):
        varss = await db.get_vars(client.me.id, "ping")
        if not varss:
            return f"Pong -"
        return str(varss)

    async def MENTION(client):
        varss = await db.get_vars(client.me.id, "mention")
        if not varss:
            return f"Client -"
        return str(varss)

    async def UPTIME(client):
        varss = await db.get_vars(client.me.id, "uptime")
        if not varss:
            return f"Alive -"
        return str(varss)

    async def PROSES(client):
        varss = await db.get_vars(client.me.id, "proses")
        if not varss:
            return f"Processing..."
        return str(varss)

    async def BROADCAST(client):
        varss = await db.get_vars(client.me.id, "gcast")
        if not varss:
            return f"Broadcast Completed!"
        return str(varss)
