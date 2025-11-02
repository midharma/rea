import asyncio

from pyrogram import Client

API_ID = input("\nMasukan API_ID:\n > ")
API_HASH = input("\nMasukan API_HASH:\n > ")


print("\n\n Masukan nomor telegram anda\n\n")

usu = Client("string", in_memory=True, api_id=API_ID, api_hash=API_HASH)


async def main():
    await usu.start()
    string = await usu.export_session_string()
    hasil = f"String anda!!\n\n`{string}`"
    try:
        await usu.send_message("me", hasil)
    except BaseException:
        pass
    print("\nJangan pernah membagikan string ini ke siapapun\n")
    print(f"\n{string}\n")
    print("\n Terima kasih\n")


asyncio.run(main())
