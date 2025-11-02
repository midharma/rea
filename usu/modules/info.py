from usu import *


PING = """Command for <b>Prefix</b>

<b>Ping</b>
 <i>Menampilkan ping</i>
    <code>{0}ping</code>"""

ALIVE = """Command for <b>Alive</b>

<b>Alive</b>
 <i>Menampilkan status userbot anda</i>
    <code>{0}alive</code>"""


INFO = """Command for <b>Info</b>

<b>Info</b>
 <i>melihat informasi data akun telegram</i>
     <code>{0}info</code> [reply/username]

 <i>melihat informasi data group/channel telegram</i>
     <code>{0}gcinfo</code> [reply/username]"""


ID = """Command for <b>ID</b>

<b>ID</b>
 <i>memeriksa id pengguna telegram</i>
    <code>{0}id</code> [reply/username]
<i>memeriksa id emoji premium telegram</i>
    <code>{0}idm</code> [reply emoji]"""


SG = """Command for <b>SG</b>

<b>SG</b>
 <i>memeriksa histori name pengguna telegram</i>
    <code>{0}sg</code> [reply/username]"""


LIMIT = """Command for <b>Limit</b>

<b>Limit bot</b>
 <i>mengecek status akun apakah terkena limit atau tidak</i>
    <code>{0}limit</code>"""

STATS = """Command for <b>Stats</b>

<b>Status</b>
 <i>melihat status akun anda</i>
    <code>{0}stats</code>"""

__UTAMA__ = "Info"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Ping", "Alive", "SG", "ID","Info", "Limit", "Stats"

__HASIL__ = PING, ALIVE, SG, ID, INFO, LIMIT, STATS

