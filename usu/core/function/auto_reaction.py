import asyncio
import random
from random import shuffle
from pyrogram import idle
from usu import *
from usu.modules import loadModule
from usu.core.helpers.help_usu import tombol_anak
from usu.core.database.local import db
from usu.core.helpers.dec import installPeer
import os
import aiorun
import traceback
import sys

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered, SessionRevoked, UserAlreadyParticipant, UserNotParticipant, UserDeactivated, UserDeactivatedBan, FloodWait)
import pytz
import pytgcalls
import pyrogram
import time
import shutil
import pytz
from datetime import datetime

async def auto_reaction_task(client, reactions):
    random_emoji = random.choice(reactions)
    reacted = set()
    try:
        try:
            peer = await client.get_chat(AUTO_REACTION)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            peer = await client.get_chat(AUTO_REACTION)
        except Exception as e:
            pass
        async for message in client.get_chat_history(peer.id, limit=1):
            if client.me.id in reacted:
                continue
            try:
                await message.react(random_emoji)
                reacted.add(client.me.id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await message.react(random_emoji)
                    reacted.add(client.me.id)
                except Exception as e:
                    pass
            except Exception as e:
                pass
    except Exception as e:
        pass


async def auto_reaction():
    reactions = ["👍", "🤩", "🎉", "😍", "👏", "🔥", "🙈", "💯", "🌚", "😎", "🍓", "🏆", "❤️‍🔥", "⚡", "🙉", "🙊", "👻", "🌭"]
    if AUTO_REACTION:
        while True:
            await asyncio.sleep(120)
            for client in tuple(ubot._ubot.values()):
                await auto_reaction_task(client, reactions)