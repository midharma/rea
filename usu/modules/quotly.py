from usu import *

STICKER = """Command for <b>Sticker</b>

<b>Sticker</b>
 <i>merubah photo/sticker/gif menjadi anime</i>
    <code>{0}toanime</code>
 <i>merubah foto menjadi sticker</i>
    <code>{0}tosticker</code>
 <i>merubah sticker/gif menjadi photo</i>
    <code>{0}toimg</code>
 <i>merubah sticker menjadi gif</i>
    <code>{0}togif</code>"""

QUOTLY = """Command for <b>Quotly</b>

<b>Quotly</b>
 <i>merubah text menjadi sticker</i>
    <code>{0}q</code> [reply text] - [colors]
 <i>menambahkan sticker ke dalam pack</i>
    <code>{0}qs</code> [reply sticker]
 <i>merubah sticker menjadi kecil</i>
    <code>{0}ting</code> [reply sticker]
 <i>merubah sticker/foto menjadi sticker text</i>
    <code>{0}mmf</code>"""


__UTAMA__ = "Stickers"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Quotly", "Sticker"

__HASIL__ = QUOTLY, STICKER

