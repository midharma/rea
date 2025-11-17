import uvloop
uvloop.install()
import asyncio

#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
import io
from contextlib import redirect_stdout
import logging
import functools
import os
import re
from aiohttp import ClientSession
from pytgcalls import PyTgCalls
from pytgcalls import filters as fl
from pyrogram import Client, filters
from pyrogram.enums import ParseMode, ChatMemberStatus
from pyrogram.handlers import CallbackQueryHandler, MessageHandler, InlineQueryHandler
from pyrogram.errors import FloodWait
from pyrogram.types import Message, BotCommand
from pyromod import listen
from rich.logging import RichHandler
from usu.config import *
import sys
import importlib
from usu.modules import loadModule
from usu import *



class ConnectionHandler(logging.Handler):
    def emit(self, record):
        error_keywords = [
            "OSError",
            "TimeoutError",
            "Too Many Open Files",
            "EMFILE",
            "[Errno 24]"
        ]
        
        message_lower = record.getMessage().lower() 

        for keyword in error_keywords:
            if keyword.lower() in message_lower:
                os.system(f"kill -9 {os.getpid()} && bash start.sh")
                break


logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.client").setLevel(logging.WARNING)
logging.getLogger("pyrogram.session.auth").setLevel(logging.CRITICAL)
logging.getLogger("pyrogram.session.session").setLevel(logging.CRITICAL)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s",
    "%d-%b %H:%M"
)

stream_handler = logging.StreamHandler()

stream_handler.setFormatter(formatter)
connection_handler = ConnectionHandler()

logger.addHandler(stream_handler)
logger.addHandler(connection_handler)



class UsuInti(Client):
    _ubot = {}
    _prefix = {}
    _translate = {}
    peer = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_prefix(self, user_id, prefix):
        self._prefix[user_id] = prefix

    async def get_prefix(self, user_id):
        return self._prefix.get(user_id, ["."])

    def cmd_prefix(self, cmd):
        command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")

        async def func(_, client, message):
            if message.text:
                text = message.text.strip().encode("utf-8").decode("utf-8")
                username = client.me.username or ""
                prefixes = await self.get_prefix(client.me.id)

                if not text:
                    return False

                for prefix in prefixes:
                    if not text.startswith(prefix):
                        continue

                    without_prefix = text[len(prefix):]

                    for command in cmd.split("|"):
                        if not re.match(
                            rf"^(?:{command}(?:@?{username})?)(?:\s|$)",
                            without_prefix,
                            flags=re.IGNORECASE | re.UNICODE,
                        ):
                            continue

                        without_command = re.sub(
                            rf"{command}(?:@?{username})?\s?",
                            "",
                            without_prefix,
                            count=1,
                            flags=re.IGNORECASE | re.UNICODE,
                        )
                        message.command = [command] + [
                            re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                            for m in command_re.finditer(without_command)
                        ]

                        return True

                return False

        return filters.create(func)


class Bot(UsuInti):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usu = None
        self.assistant = None
        self.device_model = DEVICE_NAME
        self.app_version = DEVICE_VERSION

        if STRING:
            self.usu = Client(
                name="assistant",
                in_memory=True,
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=str(STRING)
            )
            self.assistant = PyTgCalls(self.usu)

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(MessageHandler(func, filters), group)
            try:
                return func
            except Exception as e:
                logger.exception(e)
        return decorator

    def on_callback_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(CallbackQueryHandler(func, filters), group)
            try:
                return func
            except Exception as e:
                logger.exception(e)
        return decorator

    def on_inline_query(self, filters=None, group=-1):
        def decorator(func):
            self.add_handler(InlineQueryHandler(func, filters), group)
            try:
                return func
            except Exception as e:
                logger.exception(e)
        return decorator

    def usu_stream(self):
        def decorator(func):
            if not self.usu or not self.assistant:
                return
            self.assistant.on_update(fl.stream_end)(func)
            return func
        return decorator

    async def start_assistant(self):
        """Start assistant jika STRING tersedia."""
        if not self.usu or not self.assistant:
            logger.info("Assistant tidak dijalankan karena STRING kosong.")
            return

        try:
            with redirect_stdout(io.StringIO()):
                await self.usu.start()
                await self.assistant.start()
            logger.info("Assistant started!")
        except Exception as e:
            logger.error(f"[Assistant Error] {e}")
            return
        if LOGS_CHAT:
            try:
                await self.send_message(LOGS_CHAT, "<b><i>Bot aktif!</i></b>")
                await self.usu.send_message(LOGS_CHAT, "<b><i>Assistant aktif!</i></b>")
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    await self.send_message(LOGS_CHAT, "<b><i>Bot utama aktif!</i></b>")
                    await self.usu.send_message(LOGS_CHAT, "<b><i>Assistant aktif!</i></b>")
                except:
                    logger.error("Tambahkan assistant dan bot ke LOGS_CHAT dan jadikan admin.")
            except:
                logger.error("Tambahkan assistant dan bot ke LOGS_CHAT dan jadikan admin.")
                sys.exit()

    async def start(self):
        await super().start()
        await self.start_assistant()
        if LOGS_CHAT:
            get = await self.get_chat_member(LOGS_CHAT, self.me.id)
            if get.status != ChatMemberStatus.ADMINISTRATOR:
                logger.error("Tolong promosikan bot sebagai admin di logs chat")
                sys.exit()
        try:
            await self.set_bot_commands(
                [
                    BotCommand(
                        "start",
                        "mulai bot.",
                    ),
                    BotCommand(
                        "reload",
                        "reload jika bot error.",
                    ),
                    BotCommand(
                        "akses",
                        "menambahkan akses bot (Only Seller).",
                    ),
                    BotCommand(
                        "delakses",
                        "menghapus akses bot (Only Seller).",
                    ),
                    BotCommand(
                        "ping",
                        "cek bot hidup/mati",
                    ),
                    BotCommand(
                        "play",
                        "mainkan audio music",
                    ),
                    BotCommand(
                        "vplay",
                        "mainkan video music",
                    ),
                    BotCommand(
                        "playlist",
                        "daftar music yang di mainkan",
                    ),
                    BotCommand(
                        "end",
                        "hentikan music",
                    ),
                    BotCommand(
                        "skip",
                        "memutar antrian music",
                    ),
                    BotCommand(
                        "resume",
                        "lanjutkan music",
                    ),
                    BotCommand(
                        "pause",
                        "jeda music",
                    ),
                    BotCommand(
                        "all",
                        "mention semua pengguna",
                    ),
                    BotCommand(
                        "stop",
                        "mention semua pengguna",
                    ),
                    BotCommand(
                        "ankes",
                        "on/off",
                    ),
                    BotCommand(
                        "chatbot",
                        "on/off",
                    ),
                    BotCommand(
                        "bl",
                        "blacklist kata",
                    ),
                    BotCommand(
                        "unbl",
                        "unblacklist kata",
                    ),
                    BotCommand(
                        "listbl",
                        "melihat daftar kata yang di blacklist",
                    ),
                    BotCommand(
                        "addwl",
                        "tambahkan pengguna ke dalam daftar whitelist",
                    ),
                    BotCommand(
                        "delwl",
                        "hapus pengguna dari daftar whitelist",
                    ),
                    BotCommand(
                        "listwl",
                        "melihat daftar whitelist",
                    ),

                ]
            )
        except Exception as er:
            logger.error(str(er))



class Ubot(UsuInti):
    __module__ = "pyrogram.client"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.call_py = PyTgCalls(self)
        self.device_model = DEVICE_NAME
        self.app_version = DEVICE_VERSION

    def on_message(self, filters=None, group=-1):
        def decorator(func):
            for ub in self._ubot.values():
                ub.add_handler(MessageHandler(func, filters), group)
            try:
                return func
            except Exception as e:
                logger.exception(e)
        return decorator

    def usu_stream(self):
        def decorator(func):
            for ub in self._ubot.values():
                ub.call_py.on_update(fl.stream_end)(func)
            return func
        return decorator

    async def start(self):
        await super().start()
        try:
            with redirect_stdout(io.StringIO()):
                await self.call_py.start()
        except Exception as e:
            print(f"Error: {e}")
        handler = await db.get_pref(self.me.id)
        if handler:
            self._prefix[self.me.id] = handler
        else:
            self._prefix[self.me.id] = ["."]
        self._ubot[self.me.id] = self
        self._translate[self.me.id] = "id"
        logger.info(f"Client - {self.me.id} - Started!")



bot = Bot(
    name="bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True,
    workdir="./usu/",
)

ubot = Ubot(name="ubot")




from usu.core.database import *
from usu.core.function import *
from usu.core.helpers import *