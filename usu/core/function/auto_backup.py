import asyncio
import random
from usu import *
import os
import time
import shutil
import pytz
from datetime import datetime
from usu.config import DATABASE, ENCRYPTION_KEY


fernet = Fernet(ENCRYPTION_KEY)

async def auto_backup():
    db_file = f"{DATABASE}.db"
    while True:
        await asyncio.sleep(30)
        anunya = pytz.timezone("Asia/Jakarta")
        waktu = datetime.now(anunya)
        if waktu.strftime("%H:%M") == "13:00":  # jam otomatis backup
            try:
                timestamp = waktu.strftime("%Y%m%d_%H%M%S")
                backup_file = f"{DATABASE}_auto_{timestamp}.db"

                # Baca & enkripsi database
                with open(db_file, "rb") as f:
                    data = f.read()
                encrypted = fernet.encrypt(data)
                with open(backup_file, "wb") as f:
                    f.write(encrypted)

                # Kirim hasil backup terenkripsi
                for chat_id in DEVS:
                    await bot.send_document(chat_id=chat_id, document=backup_file, file_name=os.path.basename(backup_file))

                os.remove(backup_file)
                await asyncio.sleep(120)
            except Exception as e:
                logger.error(f"Auto backup error: {e}")
                if os.path.exists(backup_file):
                    os.remove(backup_file)