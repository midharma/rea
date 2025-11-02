import asyncio
import random
from usu import *
import os
import sys

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered, SessionRevoked, UserAlreadyParticipant, UserNotParticipant, UserDeactivated, UserDeactivatedBan, FloodWait)
import time
import shutil
import pytz
from datetime import datetime


async def auto_promote():
    if AUTO_PROMOTE_TEXT:
        while True:
            await asyncio.sleep(30)
            jakarta = pytz.timezone("Asia/Jakarta")
            user = await db.get_list_from_vars(bot.me.id, "user")
            group = await db.get_list_from_vars(bot.me.id, "group")
            target = []
            if datetime.now(jakarta).strftime("%H:%M") == "12:00":
                if user:
                    target.extend(user)
                if group:
                    target.extend(group)
                if target:
                    for anu in target:
                        try:
                            await bot.send_message(anu, AUTO_PROMOTE_TEXT)
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                            await bot.send_message(anu, AUTO_PROMOTE_TEXT)
                        except Exception as e:
                            pass
                    await asyncio.sleep(120)