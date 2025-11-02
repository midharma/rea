import os
import sys


TEXT_PP = f"""<b>Info Userbot AIO!

Kalian butuh Userbot minim mati - matian? tidak delay? cusss kepoin disini!

Disini kami menyediakan Userbot Custom(Request) untuk 1 Private dan Userbot satuan

Contoh Bot @InvalidSyntaxRobot dengan segala multi fungsi yang bisa membantu kalian untuk mengelola Groups seperti AntiGcast, Manage, Music, UserBot!

Fitur Utama dari UserBot ini adalah:
Admins, Broadcasts, Contents, Extras, Globals, Info, Notes, PM-Security, Sticker, Sudoers, VC-Tools

Fitur Tambahan dari UserBot ini adalah:
AntiGcast, AntiWord, Afk, Animasi, Emoji, Button, AI, Convert, Filters, Play Music(OS), Play Video(OS), Logger, Fonts, Game, Read, Reaction, Prefix, Spam, Mention, Songs dan lain - lain

Keunggulan Bot ini adalah:
• Userbot:</b>
95% Userbot tidak mati - matian menurut semua pengguna Userbot ini terkecuali ada Maintenance(Pembaruan Fitur), Sudah dipastikan Userbot ini 95% ngga delay

<b>• Bot Music:</b>
Bisa play music di group/channel

<b>• Bot AntiGcast:</b>
Membantu anda menghapus bersih gcast/broadcast yang muncul di group (metode detect)(Expert)

<b>• Bot Manage:</b>
Membantu menjaga keamanan group

<b>Harga?PM</b>
@SyntaxError404Found2"""

DEVICE_NAME = os.getenv("DEVICE_NAME", "Desktop") #Nama device bebas di ubah sesuka hati

DEVICE_VERSION = os.getenv("DEVICE_VERSION", "1.5") #Versi bebas di ubah sesuka hati

HARGA_USERBOT = int(os.getenv("HARGA_USERBOT", "25")) #Harga bebas di ubah sesuka hati

MAX_BOT = int(os.getenv("MAX_BOT", "15")) #Maksimal pengguna userbot anda

API_ID = int(os.getenv("API_ID", "29624794")) #Api ID bisa ke web my.telegram.org

API_HASH = os.getenv("API_HASH", "ccaff9da130b59e55314d6b49395a4c2") #Api Hash bisa ke web my.telegram.org

BOT_TOKEN = os.getenv("BOT_TOKEN", "8582471636:AAESpC_qjbfuasP0ZBVz--wQa9dnJBc0LtM") #Token bot

DEVS = list(map(int, os.getenv("DEVS", "2054781387 6936273085").split())) #ID akun ini full control bot

OWNER_ID = int(os.getenv("OWNER_ID", "2054781387")) #ID akun anda

AUTO_JOIN = os.getenv("AUTO_JOIN", "AIOProjectTeams CatatanHazmi").split() #Auto join semua client ke chat ini

AUTO_REACTION = os.getenv("AUTO_REACTION", None) #Auto reaction postingan channel anda

AUTO_PROMOTE_TEXT = os.getenv("AUTO_PROMOTE_TEXT", None) #Auto promote ke group dan user

USERNAME = os.getenv("USERNAME", "owchietrea") #Username akun anda

CHANNEL = os.getenv("CHANNEL", "CatatanHazmi") #Support channel

GROUP = os.getenv("GROUP", "AIOProjectTeams") #Support group

FSUB = os.getenv("FSUB", "CatatanHazmi").split() #Wajib adminkan bot di semua chat fsub ini

LOGS_CHAT = os.getenv("LOGS_CHAT", None) #Wajib adminkan bot di logs chat ini

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002579277466 -1002501848632 6904554940").split())) #Ini agar gcast yang make bot anda ga masuk ke chat tersebut

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "1b54fa62c533c2eeca60e50dadce6c0b")

GEMINI_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDnutTByS3WsTlKSaRFAyeQfm2OEQAbtvU")

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", b"V5y8fY82raviltAeUGxK6mMsNMGoiW8RYAUTna9KAbo=")

PHOTO = os.getenv("PHOTO", "https://files.catbox.moe/yptx43.jpg") #Photo bot anda

QRIS = os.getenv("QRIS", "https://files.catbox.moe/snv8qt.jpg") #foto qris anda

RMBG_API = os.getenv("RMBG_API", "KpFFVSbCqjKk8ygcthBkanFN")

DATABASE = os.getenv("DATABASE", "rea") #Nama database

STRING = os.getenv("STRING", None) #String assistant anda