import importlib
import asyncio
import random
from usu import *
from usu.modules import loadModule
from usu.core.helpers.help_usu import tombol_anak, tombol_utama
from usu.core.database.local import db
from usu.core.helpers.dec import installPeer
from usu.core.function.expired import expiredUserbots
from usu.core.function.sesi import check_session
from usu.core.function.auto_backup import auto_backup
from usu.core.function.auto_join import auto_rejoin_loop
from usu.core.function.auto_tagall import autotagall_loop
from usu.core.function.auto_reaction import auto_reaction
from usu.core.function.auto_promote import auto_promote
import os
import sys

from pyrogram.errors import (AuthKeyDuplicated, AuthKeyUnregistered, SessionRevoked, UserAlreadyParticipant, UserNotParticipant, UserDeactivated, UserDeactivatedBan, FloodWait)
import pytz
import pytgcalls
import pyrogram
import time
from datetime import datetime




async def loaded():
    for mod in loadModule():
        try:
            module = importlib.import_module(f"usu.modules.{mod}")
            imported_module = importlib.reload(module)
            utama = getattr(imported_module, "__UTAMA__", None)
            button_labels = getattr(imported_module, "__BUTTON__", None)
            text = getattr(imported_module, "__TEXT__", None)
            hasil = getattr(imported_module, "__HASIL__", None)

            if utama and button_labels and text and hasil:
                if utama not in tombol_utama:
                    tombol_utama[utama] = {"text": utama, "callback_data": f"usu {utama}", "__TEXT__": text, "HASIL": hasil}
                if utama not in tombol_anak:
                    tombol_anak[utama] = []

                buttons = []
                for label, hasil_labels in zip(button_labels, hasil):
                    callback_data = f"tousu {utama.lower()}_{label.replace(' ', '_').lower()}"
                    buttons.append({"text": label, "teks": hasil_labels, "callback_data": callback_data})

                tombol_anak[utama].extend(buttons)
        except Exception as e:
            logger.exception(f"Client - Error loading module {mod}: {e}")
    task = [installPeer, auto_reaction, expiredUserbots, check_session, auto_backup, auto_promote, autotagall_loop, auto_rejoin_loop]
    for tasks in task:
        asyncio.create_task(tasks()).add_done_callback(lambda fut: fut.exception() and logger.exception(f"Task error: {fut.exception()}"))
    jumlah_button_usu = sum(len(buttons) for buttons in tombol_anak.values())
    for anjay in DEVS:
        try:
            await bot.send_message(
                anjay,
                f"""<b><i>Userbot Active!</i></b>

<i><b>Module:</b> {jumlah_button_usu}</i>
<i><b>Jumlah Pengguna:</b> {len(ubot._ubot)}</i>
<i><b>Pyrogram:</b> {pyrogram.__version__}</i>
<i><b>Pytgcalls:</b> {pytgcalls.__version__}</i>""")
        except Exception as e:
            logger.info(f"Silahkan /start @{bot.me.username} terlebih dahulu di semua akun DEVS!")
            sys.exit()
    logger.info(f"Bot - Running!")