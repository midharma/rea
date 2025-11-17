import asyncio

from pyrogram.enums import ChatType

from usu import *
from usu.core.database.local import db

from pyrogram.errors import FloodWait, ChannelPrivate, RPCError

Chat_type = {
    "global": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL],
    "group": [ChatType.GROUP, ChatType.SUPERGROUP],
    "channel": [ChatType.CHANNEL],
    "users": [ChatType.PRIVATE],
    "all": [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.PRIVATE, ChatType.CHANNEL],
}

async def get_private_and_group_chats(client):
    user = []
    group = []
    gb = []
    channel = []
    all_chats = []
    database = await db.get_list_from_vars(client.me.id, "bcdb") or []

    try:
        async for dialog in client.get_dialogs():
            chat_id = dialog.chat.id
            chat_type_enum = dialog.chat.type
            all_chats.append(chat_id)
            try:
                if chat_type_enum == ChatType.PRIVATE:
                    user.append(chat_id)
                elif chat_type_enum in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    group.append(chat_id)
                    gb.append(chat_id)
                elif chat_type_enum == ChatType.CHANNEL:
                    channel.append(chat_id)
                    gb.append(chat_id)
            except ChannelPrivate:
                continue
            except FloodWait as e:
                await asyncio.sleep(e.value)
                if chat_type_enum == ChatType.PRIVATE:
                    user.append(chat_id)
                elif chat_type_enum in [ChatType.GROUP, ChatType.SUPERGROUP]:
                    group.append(chat_id)
                    gb.append(chat_id)
                elif chat_type_enum == ChatType.CHANNEL:
                    channel.append(chat_id)
                    gb.append(chat_id)
            except RPCError:
                continue
            except Exception:
                pass
    except Exception:
        pass

    return user, group, gb, channel, all_chats, database


async def install_my_peer(client):
    user, group, gb, channel, all_chats, database = await get_private_and_group_chats(client)
    client_id = client.me.id
    client.peer[client_id] = {"user": user, "group": group, "global": gb, "channel": channel, "all": all_chats, "db": database}


async def installPeer():
    for client_id, client in list(ubot._ubot.items()):
        try:
            await install_my_peer(client)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await install_my_peer(client)
        except Exception:
            pass