from time import time as waktunya
from usu import *
from time import time
from datetime import datetime

start_time = waktunya()


async def get_time(seconds):
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        up_time += time_list.pop() + ":"

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time



async def usu_alive():
    vars = await db.get_vars(bot.me.id, "PING_TIME")
    if not vars:
        db_ping = datetime.now().timestamp()
        await db.set_vars(bot.me.id, "PING_TIME", db_ping)
    else:
        db_ping = vars

    get_db = db_ping
    get_db_datetime = datetime.fromtimestamp(get_db)
    time_usu = datetime.now() - get_db_datetime
    total_hari = time_usu.days
    jam = time_usu.seconds // 3600
    menit = (time_usu.seconds // 60) % 60
    detik = time_usu.seconds % 60

    waktu_sekarang = ""
    if total_hari > 0:
        waktu_sekarang = f"<i>{total_hari} day(s), {jam} hour(s), {menit} minute(s)</i>"
    elif jam > 0:
        waktu_sekarang = f"<i>{jam} hour(s), {menit} minute(s)</i>"
    elif menit > 0:
        waktu_sekarang = f"<i>{menit} minute(s)</i>"
    else:
        waktu_sekarang = f"<i>Loading!</i>"

    return waktu_sekarang