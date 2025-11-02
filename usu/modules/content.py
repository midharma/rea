from usu import *


CONTENT = """Command for <b>Media-Private</b>

<b>Media private</b>
 <i>mengambil konten ch private</i>
    <code>{0}copy</code> [link]
 <i>mengambil pap timer di teruskan di pesan tersimpan akun anda</i>
    <code>{0}colong</code> [reply photo]

<b>Note:</b>
<i>gunakan fitur ini dengan sebaik - baiknya jangan di salah gunakan untuk hal negative</i>"""

EDIT = """Command for <b>Edit</b>

<b>Edit</b>
 <i>menghapus latar belakang gambar</i>
    <code>{0}rbg</code>
 <i>memberikan efek blur ke gambar</i>
    <code>{0}blur</code>
 <i>memberikan efek cermin ke gambar</i>
    <code>{0}miror</code>
 <i>memberikan efek negative ke gambar</i>
    <code>{0}negative</code>"""


ANIME = """Command for <b>Anime</b>

<b>Anime</b>
 <i>mendapatkan gambar anime secara acak</i> 
    <code>{0}wall</code>
 <i>mendapatkan gambar waifu anime</i>
    <code>{0}waifu</code>"""

IMAGE = """Command for <b>Image</b>

<b>Image</b>
 <i>mendapatkan gambar</i> 
    <code>{0}pic</code>
 <i>mendapatkan gif</i>
    <code>{0}gif</code>"""


IMGBB = """Command for <b>ImgBB</b>

<b>ImgBB</b>
 <i>upload media ke ImgBB</i>
    <code>{0}imgbb</code>"""

TG = """Command for <b>Telegraph</b>

<b>Telegraph</b>
 <i>upload media/text ke Telegraph</i>
    <code>{0}tg</code>"""




__UTAMA__ = "Contents"

__TEXT__ = f"Menu Bantuan {__UTAMA__}!"

__BUTTON__ = "Media-Private", "Edit", "Anime", "Image", "ImgBB", "Telegraph"

__HASIL__ = CONTENT, EDIT, ANIME, IMAGE, IMGBB, TG


