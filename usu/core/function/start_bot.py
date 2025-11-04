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
from datetime import datetime

async def bots():
    try:
        await bot.start()
    except FloodWait as e:
        logger.info(f"FloodWait {e.value} seconds")
        await asyncio.sleep(e.value)
        await bot.start()


async def start_bot():
    logger.info(f"Database load: {DATABASE}.db")
    asyncio.create_task(bots())