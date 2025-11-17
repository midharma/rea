import os
import shutil
from datetime import datetime
from pyrogram import Client, filters
from usu.config import DATABASE
from usu import *

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
    backup_file = f"{DATABASE}_backup_{timestamp}.db"

    try:
        shutil.copy(db_file, backup_file)
        for chat_id in DEVS:
            await bot.send_document(chat_id=chat_id, document=backup_file, file_name=backup_file)
        os.remove(backup_file)
        await usu.edit("<b><i>Backup database berhasil!</i></b>")
    except (FileNotFoundError, PermissionError, shutil.Error) as e:
        await message.reply(f"<b><i>Backup database gagal:</i></b> {e}")
        if os.path.exists(backup_file):
            os.remove(backup_file)
    except Exception as e:
        await message.reply(f"<b><i>Terjadi kesalahan tak terduga:</i></b> {e}")
    await usu.delete()

@USU.BOT("restore")
@USU.PRIVATE
@USU.DEVS
async def restore_database(client, message):
    usu = await message.reply("<b><i>Processing...</i></b>")
    reply_message = message.reply_to_message
    if not reply_message:
        await usu.edit("<b><i>Invalid!</i></b>")
        return

    db_file = f"{DATABASE}.db"
    temp_db_file = f"{DATABASE}_temp.db"
    backup = f"{DATABASE}_backup_restore.db"

    try:
        file_path = await client.download_media(reply_message)
        os.rename(file_path, temp_db_file)
        shutil.copy(db_file, backup)
        os.remove(db_file)
        os.rename(temp_db_file, db_file)
        await message.reply("<b><i>Database berhasil direstore!</i></b>")
        if os.path.exists(backup):
            os.remove(backup)
    except (FileNotFoundError, PermissionError, shutil.Error) as e:
        await message.reply(f"<b><i>Restore gagal:</i></b> {e}")
        if os.path.exists(backup):
            os.remove(db_file)
            os.rename(backup, db_file)
            await message.reply("<b><i>Restore gagal, database asli dikembalikan!</i></b>")
        if os.path.exists(temp_db_file):
            os.remove(temp_db_file)
    except Exception as e:
        await message.reply(f"<b><i>Terjadi kesalahan tak terduga:</i></b> {e}")
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
        await usu.delete()
        if result[0] != "ok":
            await message.reply("<b><i>Integritas database bermasalah. Mencoba perbaikan lebih lanjut...</i></b>")

            try:
                cursor = conn.execute("PRAGMA index_list;")
                indices = cursor.fetchall()
                for index in indices:
                    index_name = index[1]
                    conn.execute(f"REINDEX {index_name};")
                await message.reply("<b><i>Indeks diperbaiki.</i></b>")
            except Exception as e:
                await message.reply(f"<b><i>Gagal memperbaiki indeks:</i></b> {e}")

            try:
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    conn.execute(f"PRAGMA table_info({table_name});")
                await message.reply("<b><i>Tabel diperiksa.</i></b>")
            except Exception as e:
                await message.reply(f"<b><i>Gagal memeriksa tabel:</i></b> {e}")

        conn.close()
        await message.reply("<b><i>Database berhasil diperbaiki!</i></b>")

    except sqlite3.DatabaseError as e:
        await message.reply(f"<b><i>Perbaikan database gagal:</i></b> {e}")
        if os.path.exists(db_file):
            os.remove(db_file)
            os.rename(backup_file, db_file)
            await message.reply("<b><i>Perbaikan gagal, database asli dikembalikan!</i></b>")
    except Exception as e:
        await message.reply(f"<b><i>Terjadi kesalahan tak terduga:</i></b> {e}")
    finally:
        if os.path.exists(backup_file):
            os.remove(backup_file)