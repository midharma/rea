import asyncio
import random
from usu import *
import os

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered, SessionRevoked, UserAlreadyParticipant, UserNotParticipant, UserDeactivated, UserDeactivatedBan, FloodWait)
import time
import shutil
import pytz
from datetime import datetime


async def join_auto_chats(ubot_):
    for auto in AUTO_JOIN:
        try:
            await ubot_.join_chat(auto)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await ubot_.join_chat(auto)
        except UserAlreadyParticipant:
            continue
        except Exception as e:
            continue

async def auto_rejoin_loop():
    if AUTO_JOIN:
        while True:
            await asyncio.sleep(120)
            for ubot_ in tuple(ubot._ubot.values()):
                await join_auto_chats(ubot_)