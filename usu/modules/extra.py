from usu import *

HELP_CUSTOM = """Command for <b>Help Custom</b>

<b>Help Custom</b>
 <i>menambahkan foto pada inline help</i>
    <code>{0}sethelp</code> [reply_photo/reply_video/none]"""

DOWN = """Command for <b>Songs</b>

<b>Songs</b>
 <i>mendownload music youtube yang di inginkan</i>
    <code>{0}song</code> [title]
 <i>mendownload video youtube yang di inginkan</i>
    <code>{0}vsong</code> [title]"""

CONVERT = """Command for <b>Convert</b>

<b>Convert</b>
 <i>untuk merubah video menjadi audio mp3</i>
    <code>{0}toaudio</code>"""


EMO_ = """Command for <b>Emoji Mode</b>

<b>Query:</b>
  <code>|pong |alive |client</code>
  <code>|gcast |sukses |gagal</code>
  <code>|proses |menunggu |catatan</code>

<b>Emoji Mode</b>
 <i>mengubah emoji pada bot</i>
    <code>{0}emoji</code> [query] [emoji/none]
 <i>mengaktifkan/nonaktifkan emoji mode pada bot</i>
    <code>{0}emoji</code> [on/off]"""


TEXT_CUSTOM = """Command for <b>Text Settings</b>

<b>Query:</b>
  <code>|pong |alive |client</code>
  <code>|gcast |proses</code>

<b>Text Settings</b>
 <i>mengubah text pada bot</i>
    <code>{0}text</code> [query] [text/none]"""


INLINE_MODE = """Command for <b>Inline Mode</b>

<b>Inline Mode</b>
 <i>mengaktifkan/nonaktifkan inline mode pada bot</i>
    <code>{0}inline</code> [on/off]"""


RESELLER = """Command for <b>Reseller Userbot</b>

<b>Reseller</b>
 <i>memberikan akses bot</i>
    <code>{0}akses</code> [username/user id]

 <i>melepas akses bot</i>
    <code>{0}delakses</code> [username/user id]

<b>Notes:</b>
<i>Perintah ini untuk seller userbot</i>"""


ADZAN = """Command for <b>Adzan</b>

<b>Adzan</b>
 <i>melihat jadwal adzan di lokasi anda</i>
    <code>{0}adzan</code> [nama kota]"""

ABSEN = """Command for <b>Absen</b>

<b>Absen</b>
 <i>Menampilkan absen bot</i>
    <code>{0}absen</code>

 <i>Menghapus absen bot</i>
    <code>{0}clearabsen</code>"""

AFK = """Command for AFK

mengaktifkan away from keyboard
   {0}afk [alasan]

menonaktifkan away from keyboard
   {0}unafk

Notes:
jika afk aktif bot akan otomatis merespon
dimana anda di tandai seseorang"""

ANIMASI = """Command for <b>Animasi</b>

<b>Animals Text</b>
 <i>melakukan text animasi bergerak</i>
    <code>{0}dino |{0}nakal |{0}loveyou</code>
    <code>{0}ange |{0}kocok |{0}lipkol</code>
    <code>{0}hack |{0}syg |{0}rumah</code>
    <code>{0}tq</code>

<b>Animals Picture</b>
 <i>melakukan animasi gambar</i>
    <code>{0}kntl |{0}ajg |{0}tembak</code>
    <code>{0}heli |{0}nah |{0}spongeboob</code>
    <code>{0}piss |{0}hmm |{0}bundir</code>
    <code>{0}tank |{0}awk |{0}y</code>"""

ARCHIVE = """Command for <b>Archive</b>

<b>Type</b>
 <code>'users'</code> , arsip semua pm
 <code>'group'</code> , arsip semua group
 <code>'channel'</code> , arsip semua channel 
 <code>'all'</code> , arsip semua

<b>Archives</b>
 <i>mengarsipkan obrolan group/users/bot</i>
    <code>{0}archiveall</code> [type]
 <i>menghapus arsip obrolan group/users/bot</i>
    <code>{0}unarchiveall</code> [type]"""

BACA = """Command for <b>Baca</b>

<b>Type</b>
 <code>'group'</code> , baca semua group
 <code>'channel'</code> , baca semua channel
 <code>'all'</code> , baca semua pesan
 <code>'users'</code> , baca semua users 

<b>Baca</b>
 <i>membaca obrolan group/users/channel</i>
    <code>{0}read or {0}baca</code> [type]"""


BUTTON = """Command for <b>Button</b>

<b>Create Button</b>
 <i>Membuat button</i>
    <code>{0}button</code>

<b>Example:</b>
<code>{0}button</code> text ~> button_text:button_link"""


CREAT = """Command for <b>Creat</b>

<b>Type:</b>
<code>'channel'</code> , membuat channel
<code>'group'</code> , membuat group

<b>Create</b>
 <i>membuat sebuah group/channel baru</i>
    <code>{0}creat</code> [type]"""

BIO = """Command for <b>Set-Bio</b>

<b>Bio</b>
 <i>mengubah bio pada akun anda</i>
    <code>{0}setbio</code> [text]"""

NAME = """Command for <b>Set-Name</b>

<b>Name</b>
 <i>mengubah nama pada akun anda:</i>
    <code>{0}setname</code> [name]"""

PP = """Command for <b>Set-Profile</b>

<b>Profile</b>
 <i>mengubah foto pada akun anda:</i>
    <code>{0}setpp</code> [reply]"""

BLOCKS = """Command for <b>Blocks</b>

<b>Blocks</b>
 <i>memblokir pengguna</i>
    <code>{0}block</code>
 <i>membuka pemblokiran pengguna</i>
    <code>{0}unblock</code>"""


ASK = """Command for <b>Chat-GPT</b>

<b>AI</b>
 <i>mengajukan pertanyaan ke AI</i>
    <code>{0}ask or {0}ai</code> [question]

<b>Example:</b>
<code>{0}ask</code> kapan indonesia merdeka?"""

GEMINI = """Command for <b>Gemini-AI</b>

<b>Gemini</b>
 <i>mengajukan pertanyaan ke AI</i>
    <code>{0}gemini</code> [question]

<b>Example:</b>
<code>{0}gemini</code> kapan indonesia merdeka?"""

PREFIX = """Command for <b>Prefix</b>

<b>Prefix Handler</b>
 <i>Mengganti handler perintah</i>
    <code>{0}sp</code> [handler]

 <i>Jika lupa handler perintah, bisa reset di bot nya</i>  """


REP = """Command for <b>Filters</b>

<b>Command Filters in group</b>
 <i>Mengaktifkan filter </i>
  <code>{0}filter</code> [ON or OFF]

 <i>Menambahkan kata yang ingin di filter </i>
  <code>{0}addfilter</code> [nama filter] [text/reply]

 <i>Menampilkan daftar kata yang di filter</i>
  <code>{0}filters</code>

 <i>Menghapus kata yang di filter</i>
  <code>{0}delfilter</code> [nama filter]

 <i>Menghapus semua kata yang di filter</i>
  <code>{0}clearfilter</code>"""

GAME = """Document for <b>Game</b>

<b>Games</b>
 <i>permainan catur</i>
    <code>{0}catur</code>
<i>permainan random telegram</i>
    <code>{0}game</code>

<b>Note:</b> 
<i>jumlah game yang akan di munculkan 500+ jenis game yang keluar berbeda - beda </i>"""


INVITE = """Command for <b>Invite</b>

<b>Inviting</b>
 <i>mengundang anggota ke group</i>
    <code>{0}invite</code> [username]
<i>mengundang beberapa anggota dari group lain</i>
    <code>{0}inviteall</code> [username]
<i>membatalkan perintah inviteall</i>
    <code>{0}cancelinvite</code>"""


JOINLEAVE = """Command for <b>JoinLeave</b>

<b>Joinned</b>
 <i>bergabung group</i>
    <code>{0}join</code> [username/tautan]

<b>Leave</b>
 <i>keluar dari group itu sendiri</i>
    <code>{0}kickme</code>
 <i>keluar dari semua chat</i>
    <code>{0}leaveall</code> [group/channel/users]"""


LOGGER = """Document for <b>Logger</b>

<b>Logger</b>
 <i>mengaktifkan atau menonaktifkan logger</i>
    <code>{0}logger</code> [on/off]"""

FONTS = """Command for <b>Fonts</b>

<b>Fonts</b>
 <i>merubah text menjadi berbeda</b>
    <code>{0}font</code>"""

CARBONS = """Command for <b>Carbons</b>

<b>Carbons</b>
 <i>membuat text carbonara</i>
    <code>{0}carbon</code>"""

BAR = """Command for <b>BarCodes</b>
    
<b>BarCodes</b>
 <i>merubah qrcode text menjadi gambar</i>
    <code>{0}qrGen</code>
 <i>merubah qrcode media menjadi text</b>
    <code>{0}qrRead</code>"""


PURGE = """Command for <b>Purge</b>

<b>Delete message</b>
 <i>hapus semua pesan dari pesan yang di reply</i>
    <code>{0}purge</code>
 <i>menghapus pesan anda sediri</i>
    <code>{0}purgeme</code> [jumlah]"""


REACT = """Command for <b>Reaction</b>

<i>memberikan reaction emoji</i>
   <code>{0}react</code> [username]

<i>membatalkan proses reaction</i>
   <code>{0}cancelreact</code>
   
<b>Note</b>
<i>hanya bisa emot bukan emoji dan dapat di lakukan menggunakan username group/user</i>"""


TAGALL = """Command for <b>TagAll</b>

<b>Mentions</b>
 <i>mention semua anggota group</i>
    <code>{0}tagall or {0}all</code>
 <i>membatalkan perintah mention</i>
    <code>{0}cancel</code>"""


KASAR = """Command for <b>Animasi</b>

<b>Animals text hatred</b>
 <i>melakukan animasi text bergerak kata kasar</i>
    <code>{0}ngentot |{0}ngatain |{0}goblok</code>
    <code>{0}yatim |{0}kontol |{0}hina</code>
    <code>{0}ngaca |{0}alay |{0}santet</code>"""


TR = """Command for <b>Translate</b>

<b>Change language</b>
 <i>menerjemahkan pesan/text</i>
    <code>{0}tr</code> [reply] [singkatan negara]
 <i>merubah text menjadi pesan suara sesuai bahasa</i>
    <code>{0}tts</code> [text]"""


SECRET = """Command for <b>Secret</b>

<b>Anonims</b>
 <i>mengirim pesan secara rahasia</i>
    <code>{0}msg</code> [reply to user - text]"""

SPAM = """Command for <b>Spam</b>

<b>Spams</b>
 <i>melakukan spam pesan</i>
    <code>{0}spam</code> [text] [jumlah]
 <i>mengatur delay setiap pesan yang di kirim</i>
    <code>{0}setdelay</code> [delay]
 <i>cancel spam pesan</i>
    <code>{0}cancelspam</code>"""


ADMINLIST = """Command for <b>Adminlist</b>

<b>Adminlist</b>
 <i>cek admin group</i> 
    <code>{0}adminlist</code>"""

BOTLIST = """Command for <b>Botlist</b>

<b>Botlist</b>
 <i>cek bot group</i> 
    <code>{0}botlist</code>"""

NULIS = """Command for <b>Nulis</b>

<b>Nulis</b>
 <i>menulis sesuatu</i>
    <code>{0}nulis</code> [text]"""

__UTAMA__ = "Extras"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Logger", "Emoji Mode", "Prefix", "Translate", "Chat-GPT", "Gemini-AI", "Absen", "Adzan", "Afk", "Admin List", "Bot List", "Animasi", "Kasar", "Archive", "Spam", "Read", "Button", "Creat", "Blocks", "Filters", "Game", "Invite", "Joinleave", "Fonts", "Carbons","BarCodes", "Purge", "React", "Tagall", "Secret", "Set-Profile", "Set-Name", "Set-Bio", "Reseller", "Nulis", "Songs", "Convert", "Text Custom", "Inline Mode", "Help Custom"

__HASIL__ = LOGGER, EMO_, PREFIX, TR, ASK, GEMINI, ABSEN, ADZAN, AFK, ADMINLIST, BOTLIST, ANIMASI, KASAR, ARCHIVE, SPAM, BACA, BUTTON, CREAT, BLOCKS, REP, GAME, INVITE, JOINLEAVE, FONTS, CARBONS, BAR, PURGE, REACT, TAGALL, SECRET, PP, NAME, BIO, RESELLER, NULIS, DOWN, CONVERT, TEXT_CUSTOM, INLINE_MODE, HELP_CUSTOM



