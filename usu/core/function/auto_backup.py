import asyncio
import random
from usu import *
import os
import time
import shutil
import pytz
from datetime import datetime


async def auto_backup():
    db_file = f"{DATABASE}.db"
    while True:
        await asyncio.sleep(30)
        anunya = pytz.timezone("Asia/Jakarta")
        waktu = datetime.now(anunya)
        if waktu.strftime("%H:%M") == "13:00":
            try:
                timestamp = waktu.strftime("%Y%m%d_%H%M%S")
                backup_file = f"{DATABASE}_backup_{timestamp}.db"
                shutil.copy(db_file, backup_file)
                for chat_id in DEVS:
                    await bot.send_document(chat_id=chat_id, document=backup_file, file_name=backup_file)
                os.remove(backup_file)
                await asyncio.sleep(120)
            except Exception as e:
                logger.error(f"Error: {e}")
                if os.path.exists(backup_file):
                    os.remove(backup_file)