import asyncio
import random
from random import shuffle
from pyrogram import idle
from usu import *
from usu.modules import loadModule
from usu.core.helpers.help_usu import tombol_anak
from usu.core.database.local import db
from usu.core.helpers.dec import installPeer
from usu.core.helpers.tools import bash
import os
import aiorun
import traceback
import sys

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered, SessionRevoked, UserAlreadyParticipant, UserNotParticipant, UserDeactivated, UserDeactivatedBan, FloodWait)
import pytgcalls
import pyrogram
import time
import shutil
import pytz
from datetime import datetime

async def start_and_join(ubot_):
    await ubot_.start()
    if AUTO_JOIN:
        await join_auto_chats(ubot_)

"""async def start_ubot():
    for data in await db.get_userbots():
        try:
            await start_and_join(Ubot(**data))
        except Exception as e:
            pass
    logger.info(f"Successfully started {len(ubot._ubot)} client!")"""

async def start_ubot():
    userbots = await db.get_userbots()
    tasks = []

    for data in userbots:
        try:
            tasks.append(asyncio.create_task(start_and_join(Ubot(**data))))
        except Exception as e:
            logger.error(f"Gagal membuat task: {e}")

    await asyncio.gather(*tasks, return_exceptions=True)
    #await bash(f"rm -rf *session*")
    logger.info(f"Successfully started {len(ubot._ubot)} client!")