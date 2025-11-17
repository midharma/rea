import asyncio
from usu import *
import time
from usu.core.function.start_ubot import start_ubot
from usu.core.function.start_bot import start_bot
from usu.core.function.auto_load import loaded
from usu.core.function.patch_pyrogram import apply_patch


async def stop_hazmi():
    for target in ubot._ubot.values():
        try:
            await target.stop()
        except Exception as e:
            pass
    try:
        await bot.stop()
    except Exception as e:
        pass

async def start_hazmi():
    await start_bot()
    await start_ubot()
    await loaded()
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    #apply_patch()
    restart_delay = 5
    loop = asyncio.get_event_loop()

    while True:
        try:
            loop.run_until_complete(start_hazmi())
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Dihentikan manual.")
            loop.run_until_complete(stop_hazmi())
            break
        except Exception as e:
            logger.exception(f"💥 Terjadi error: {e}")
            logger.info(f"🔁 Restarting dalam {restart_delay} detik...")
            time.sleep(restart_delay)

"""async def start_hazmi():
    asyncio.create_task(bots())
    asyncio.create_task(start_ubot())
    await loaded()


if __name__ == "__main__":
    restart_delay = 5
    while True:
        try:
            loop = asyncio.get_event_loop()
            hazmi_run = loop.create_task(start_hazmi())
            loop.run_until_complete(hazmi_run)
            # jika ingin menjalankan start_hazmi terus menerus tanpa akhir
            # loop.run_forever()
            break
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Dihentikan manual.")
            break
        except Exception as e:
            logger.error(f"💥 Terjadi error: {e}")
            logger.info(f"🔁 Restarting dalam {restart_delay} detik...")
            time.sleep(restart_delay)"""

"""if __name__ == "__main__":
    restart_delay = 5
    while True:
        try:
            aiorun.run(
                start_hazmi(),
                loop=bot.loop
            )
            break
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Dihentikan manual.")
            break
        except Exception as e:
            logger.error(f"💥 Terjadi error: {e}")
            logger.info(f"🔁 Restarting dalam {restart_delay} detik...")
            time.sleep(restart_delay)"""


"""if __name__ == "__main__":
    restart_delay = 5

    while True:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        task = loop.create_task(start_hazmi())

        try:
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            logger.info("🛑 Dihentikan manual.")
            try:
                task.cancel()
                loop.run_until_complete(task)
            except Exception as cancel_err:
                logger.warning(f"⚠️ Gagal membatalkan task (exit): {cancel_err}")
            break  # keluar dari while True
        except Exception as e:
            logger.error(f"💥 Terjadi error: {e}")
            logger.info(f"🔁 Restarting dalam {restart_delay} detik...")

            try:
                task.cancel()
                loop.run_until_complete(task)
            except Exception as cancel_err:
                logger.warning(f"⚠️ Gagal membatalkan task (restart): {cancel_err}")

            time.sleep(restart_delay)
        finally:
            loop.stop()
            loop.close()"""


