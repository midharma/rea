import os
import shutil
import sqlite3
from datetime import datetime
from cryptography.fernet import Fernet
from usu.config import DATABASE, ENCRYPTION_KEY
from usu import *


fernet = Fernet(ENCRYPTION_KEY)

@USU.BOT("backup")
@USU.PRIVATE
@USU.DEVS
async def backup_database(client, message):
    usu = await message.reply("<b><i>Processing...</i></b>")
    db_file = f"{DATABASE}.db"
    if not os.path.exists(db_file):
        await usu.edit("<b><i>File database tidak ditemukan!</i></b>")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{DATABASE}_backup_{timestamp}.db"  # tetap .db walau terenkripsi

    try:
        # Baca file database dan enkripsi
        with open(db_file, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)

        with open(backup_file, "wb") as f:
            f.write(encrypted)

        # Kirim file backup terenkripsi ke DEVS
        for chat_id in DEVS:
            await bot.send_document(chat_id=chat_id, document=backup_file, file_name=os.path.basename(backup_file))

        os.remove(backup_file)
        await usu.edit("<b><i>Backup database terenkripsi (.db) berhasil dikirim!</i></b>")
    except Exception as e:
        await message.reply(f"<b><i>Backup database gagal:</i></b> {e}")
        if os.path.exists(backup_file):
            os.remove(backup_file)
    await usu.delete()


@USU.BOT("restore")
@USU.PRIVATE
@USU.DEVS
async def restore_database(client, message):
    usu = await message.reply("<b><i>Processing...</i></b>")
    reply_message = message.reply_to_message
    if not reply_message:
        await usu.edit("<b><i>Balas file backup (.db terenkripsi) untuk merestore!</i></b>")
        return

    db_file = f"{DATABASE}.db"
    temp_enc = f"{DATABASE}_temp.db"
    backup = f"{DATABASE}_backup_before_restore.db"

    try:
        # Download file terenkripsi
        file_path = await client.download_media(reply_message)
        os.rename(file_path, temp_enc)

        # Backup database lama
        if os.path.exists(db_file):
            shutil.copy(db_file, backup)

        # Dekripsi dan tulis ulang ke file utama
        with open(temp_enc, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(db_file, "wb") as f:
            f.write(decrypted_data)

        await message.reply("<b><i>Database terenkripsi (.db) berhasil direstore!</i></b>")

        if os.path.exists(backup):
            os.remove(backup)
        if os.path.exists(temp_enc):
            os.remove(temp_enc)

    except Exception as e:
        await message.reply(f"<b><i>Restore gagal:</i></b> {e}")
        # Kembalikan database lama jika gagal
        if os.path.exists(backup):
            if os.path.exists(db_file):
                os.remove(db_file)
            os.rename(backup, db_file)
            await message.reply("<b><i>Database asli telah dikembalikan!</i></b>")
        if os.path.exists(temp_enc):
            os.remove(temp_enc)
    await usu.delete()


@USU.BOT("repair")
@USU.PRIVATE
@USU.DEVS
async def repair_database(client, message):
    usu = await message.reply("<b><i>Processing...</i></b>")
    db_file = f"{DATABASE}.db"
    backup_file = f"{DATABASE}_repair_backup.db"

    if not os.path.exists(db_file):
        await usu.edit("<b><i>File database tidak ditemukan!</i></b>")
        return

    try:
        shutil.copy(db_file, backup_file)
        conn = sqlite3.connect(db_file)
        conn.execute("VACUUM;")
        cursor = conn.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()

        if result[0] != "ok":
            await message.reply("<b><i>Integritas database bermasalah, mencoba memperbaiki...</i></b>")
            try:
                cursor = conn.execute("PRAGMA index_list;")
                indices = cursor.fetchall()
                for index in indices:
                    index_name = index[1]
                    conn.execute(f"REINDEX {index_name};")
                await message.reply("<b><i>Indeks diperbaiki.</i></b>")
            except Exception as e:
                await message.reply(f"<b><i>Gagal memperbaiki indeks:</i></b> {e}")
        conn.close()
        await message.reply("<b><i>Database berhasil diperbaiki!</i></b>")

    except sqlite3.DatabaseError as e:
        await message.reply(f"<b><i>Perbaikan database gagal:</i></b> {e}")
        if os.path.exists(backup_file):
            os.remove(db_file)
            os.rename(backup_file, db_file)
            await message.reply("<b><i>Database asli dikembalikan!</i></b>")
    except Exception as e:
        await message.reply(f"<b><i>Terjadi kesalahan tak terduga:</i></b> {e}")
    finally:
        if os.path.exists(backup_file):
            os.remove(backup_file)
    await usu.delete()
