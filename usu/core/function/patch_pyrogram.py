import re
import inspect
import traceback
from functools import wraps
from typing import Union

from pyrogram import Client, parser, raw, utils
from pyrogram.errors import PeerIdInvalid
from pyrogram.handlers import RawUpdateHandler
from pyrogram import ContinuePropagation


class ResolvePeerPatch:
    @staticmethod
    async def resolve_peer(self: "Client", peer_id: Union[int, str]):
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        try:
            return await self.storage.get_peer_by_id(peer_id)
        except KeyError:
            # jika peer_id string
            if isinstance(peer_id, str):
                if peer_id in ("self", "me"):
                    return raw.types.InputPeerSelf()
                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())
                peer_id = re.sub(r"https://t.me/", "", peer_id)

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return await self.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        r = await self.invoke(
                            raw.functions.contacts.ResolveUsername(username=peer_id)
                        )
                        await self.fetch_peers(r.chats + r.users)
                        return await self.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return await self.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid

            # fallback numeric ID
            if isinstance(peer_id, int):
                # user
                if peer_id > 0:
                    users = await self.invoke(
                        raw.functions.users.GetUsers(
                            id=[raw.types.InputUser(user_id=peer_id, access_hash=0)]
                        )
                    )
                    await self.fetch_peers(users)

                # supergroup/channel (negatif)
                elif peer_id < 0:
                    if str(peer_id).startswith("-100"):
                        channel_id = int(str(peer_id)[4:])  # hapus prefix -100
                        channels = await self.invoke(
                            raw.functions.channels.GetChannels(
                                id=[raw.types.InputChannel(channel_id=channel_id, access_hash=0)]
                            )
                        )
                        await self.fetch_peers(channels.chats)
                    else:
                        # group legacy (ID negatif tapi bukan supergroup)
                        chats = await self.invoke(raw.functions.messages.GetChats(id=[-peer_id]))
                        await self.fetch_peers(chats.chats)

            # ambil ulang dari storage
            try:
                return await self.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid

# -----------------------------
# Silent handler_worker patch (fix ContinuePropagation)
# -----------------------------
async def silent_handler_worker(self, lock):
    while True:
        packet = await self.updates_queue.get()
        if packet is None:
            break
        try:
            update, users, chats = packet
            parser_fn = self.update_parsers.get(type(update), None)
            parsed_update, handler_type = (
                await parser_fn(update, users, chats)
                if parser_fn is not None else (None, type(None))
            )
            async with lock:
                for group in self.groups.values():
                    for handler in group:
                        args = None
                        if isinstance(handler, handler_type):
                            try:
                                if await handler.check(self.client, parsed_update):
                                    args = (parsed_update,)
                            except Exception:
                                continue
                        elif isinstance(handler, RawUpdateHandler):
                            args = (update, users, chats)
                        if args is None:
                            continue
                        try:
                            if inspect.iscoroutinefunction(handler.callback):
                                await handler.callback(self.client, *args)
                            else:
                                await self.loop.run_in_executor(
                                    self.client.executor,
                                    handler.callback,
                                    self.client,
                                    *args
                                )
                        except ContinuePropagation:
                            # biarkan handler lain tetap diproses
                            continue
                        except Exception:
                            continue
                        break
        except Exception:
            continue


# -----------------------------
# Safe handle_updates patch
# -----------------------------
async def safe_handle_updates(self, *args, **kwargs):
    try:
        return await self._old_handle_updates(*args, **kwargs)
    except (ValueError, KeyError) as e:
        if "Peer id invalid" in str(e) or "ID not found" in str(e):
            return None
        raise e



# -----------------------------
# Apply all patches runtime
# -----------------------------
def apply_patch():
    # ResolvePeer
    Client.resolve_peer = ResolvePeerPatch.resolve_peer
    # Handler worker
    from pyrogram.dispatcher import Dispatcher

    Dispatcher.handler_worker = silent_handler_worker
    # Handle updates
    if not hasattr(Client, "_old_handle_updates"):
        Client._old_handle_updates = Client.handle_updates
    Client.handle_updates = safe_handle_updates