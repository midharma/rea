import json

import requests
from pyrogram import filters
from usu import *




@USU.UBOT("adzan")
async def adzan_shalat(client: Client, message: Message):
    sks = await EMO.SUKSES(client)
    ggl = await EMO.GAGAL(client)
    prs = await EMO.PROSES(client)
    broad = await EMO.BROADCAST(client)
    ptr = await EMO.PUTARAN(client)
    if len(message.command) > 1:
        LOKASI = message.text.split(" ", 1)[1]
    else:
        LOKASI = "Banjarmasin"
    url = f"http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc"
    request = requests.get(url)
    if request.status_code != 200:
        await message.reply(f"<b><i>Maaf Tidak Menemukan Kota {LOKASI}</i></b>")
    result = json.loads(request.text)
    if 'items' in result:
        usu = f"""
<i><b>Jadwal adzan</b>
<b>Tanggal</b> <code>{result['items'][0]['date_for']}</code>
<b>Kota</b> <code>{result['query']} | {result['country']}</code>

<b>Terbit  :</b> <code>{result['items'][0]['shurooq']}</code>
<b>Subuh   :</b> <code>{result['items'][0]['fajr']}</code>
<b>Dzuhur  :</b> <code>{result['items'][0]['dhuhr']}</code>
<b>Ashar   :</b> <code>{result['items'][0]['asr']}</code>
<b>Maghrib :</b> <code>{result['items'][0]['maghrib']}</code>
<b>Isya    :</b> <code>{result['items'][0]['isha']}</code></i>"""
    else:
        usu = f"<b><i>{ggl}Error!</i></b>"
    await message.reply(usu)
