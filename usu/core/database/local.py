import sqlite3
import os
import sys
import json
from datetime import datetime, timezone
import dateutil.parser
import pytz
from usu.config import DATABASE, ENCRYPTION_KEY
from cryptography.fernet import Fernet, InvalidToken

class DatabaseUsu:
    def __init__(self, db_name):
        # db_name: name without .db
        self.db_name = os.path.join(os.getcwd(), f"{db_name}.db")
        self.conn = None

        # init fernet
        if not ENCRYPTION_KEY:
            logger.exception("ENCRYPTION_KEY tidak ditemukan di config. Generate dulu dengan run python3 genkey.py")
            sys.exit()
        self.fernet = Fernet(ENCRYPTION_KEY)

        self._initialize_connection()

    # -------- helpers encryption --------
    def _encrypt(self, plaintext: str) -> str:
        if plaintext is None:
            return None
        token = self.fernet.encrypt(plaintext.encode("utf-8"))
        return token.decode("utf-8")

    def _decrypt(self, token_text: str) -> str:
        if token_text is None:
            return None
        try:
            plain = self.fernet.decrypt(token_text.encode("utf-8"))
            return plain.decode("utf-8")
        except InvalidToken:
            logger.error("Invalid encryption token: gagal dekripsi (token salah atau korup).")
            return None
        except Exception as e:
            logger.error(f"Gagal dekripsi: {e}")
            return None

    # -------- DB init --------
    def _initialize_connection(self):
        db_directory = os.path.dirname(self.db_name)
        if db_directory and not os.path.exists(db_directory):
            try:
                os.makedirs(db_directory, exist_ok=True)
            except OSError as e:
                logger.exception(f"Gagal membuat direktori database '{db_directory}': {e}")
        if db_directory and not os.access(db_directory, os.W_OK):
            logger.exception(f"Tidak ada izin tulis untuk direktori database: {db_directory}. Mohon periksa izin folder.")
            # os.system(f"kill -9 {os.getpid()} && bash start.sh")
        try:
            # check_same_thread=False agar bisa dipanggil dari thread lain jika perlu
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            cursor = self.conn.cursor()
            self._create_tables(cursor)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.exception(f"Terjadi kesalahan saat menginisialisasi database: {e}")
            # os.system(f"kill -9 {os.getpid()} && bash start.sh")

    def _create_tables(self, cursor):
        tables = {
            "vars": "user_id TEXT PRIMARY KEY, vars_data TEXT",
            "ubot": "user_id TEXT PRIMARY KEY, ubot_data TEXT",
            "prefixes": "user_id TEXT PRIMARY KEY, user_data TEXT",
            "twofactor": "user_id TEXT PRIMARY KEY, user_data TEXT",
            "users": "user_id TEXT PRIMARY KEY, user_data TEXT"
        }
        for table_name, columns in tables.items():
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    def get_connection(self):
        if self.conn is None:
            self._initialize_connection()
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info(f"Koneksi database ke {self.db_name} telah ditutup.")

    # -------- helpers read/write encrypted JSON in column --------
    def _read_json_from_col(self, cursor_row):
        """
        Mengambil hasil fetchone() yang mengandung 1 kolom encoded.
        Mengembalikan dict atau None.
        """
        if cursor_row is None:
            return None
        # cursor_row bisa berupa sqlite3.Row; ambil kolom pertama
        encoded = cursor_row[0] if len(cursor_row) > 0 else None
        if not encoded:
            return None
        decrypted = self._decrypt(encoded)
        if decrypted is None:
            return None
        try:
            return json.loads(decrypted)
        except Exception as e:
            logger.exception(f"Gagal json.loads setelah dekripsi: {e}")
            return None

    def _write_json_to_col(self, cursor, table, user_id, col_name, obj):
        """
        Serialize obj -> encrypt -> INSERT OR REPLACE ke table(col_name)
        """
        json_data = json.dumps(obj)
        encrypted = self._encrypt(json_data)
        cursor.execute(
            f"INSERT OR REPLACE INTO {table} (user_id, {col_name}) VALUES (?, ?)",
            (user_id, encrypted)
        )

    # ----------------- vars operations -----------------
    async def set_vars(self, user_id, vars_name, value, query="vars"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT vars_data FROM vars WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
        else:
            data = {}

        if query not in data:
            data[query] = {}
        data[query][vars_name] = value

        self._write_json_to_col(cursor, "vars", user_id, "vars_data", data)
        conn.commit()

    async def get_vars(self, user_id, vars_name, query="vars"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT vars_data FROM vars WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            data = self._read_json_from_col(row) or {}
            return data.get(query, {}).get(vars_name)
        return None

    async def remove_vars(self, user_id, vars_name, query="vars"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT vars_data FROM vars WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
            if query in data and vars_name in data[query]:
                del data[query][vars_name]
                self._write_json_to_col(cursor, "vars", user_id, "vars_data", data)
                conn.commit()

    async def all_vars(self, user_id, query="vars"):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT vars_data FROM vars WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            data = self._read_json_from_col(result) or {}
            return data.get(query)
        return None

    async def remove_all_vars(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vars WHERE user_id = ?", (user_id,))
        conn.commit()

    async def get_list_from_vars(self, user_id, vars_name, query="vars"):
        vars_data = await self.get_vars(user_id, vars_name, query)
        if isinstance(vars_data, list):
            return vars_data
        if vars_data is None:
            return []
        return [vars_data]

    async def add_to_vars(self, user_id, vars_name, value, query="vars"):
        existing = await self.get_list_from_vars(user_id, vars_name, query)
        if value not in existing:
            existing.append(value)
            await self.set_vars(user_id, vars_name, existing, query)

    async def remove_from_vars(self, user_id, vars_name, value, query="vars"):
        vars_list = await self.get_list_from_vars(user_id, vars_name, query)
        if value in vars_list:
            vars_list.remove(value)
            await self.set_vars(user_id, vars_name, vars_list, query)

    async def get_pm_id(self, user_id):
        pm_id = await self.get_vars(user_id, "PM_PERMIT")
        return [int(x) for x in str(pm_id).split()] if pm_id else []

    async def add_pm_id(self, me_id, user_id):
        pm_id = await self.get_vars(me_id, "PM_PERMIT")
        if pm_id:
            user_id = f"{pm_id} {user_id}"
        await self.set_vars(me_id, "PM_PERMIT", user_id)

    async def remove_pm_id(self, me_id, user_id):
        pm_id = await self.get_vars(me_id, "PM_PERMIT")
        if pm_id:
            list_id = [int(x) for x in str(pm_id).split() if x != str(user_id)]
            await self.set_vars(me_id, "PM_PERMIT", " ".join(map(str, list_id)))

    # ----------------- ubot operations -----------------
    async def add_ubot(self, user_id, api_id, api_hash, session_string):
        conn = self.get_connection()
        cursor = conn.cursor()
        data = {
            "api_id": api_id,
            "api_hash": api_hash,
            "session_string": session_string,
        }
        self._write_json_to_col(cursor, "ubot", user_id, "ubot_data", data)
        conn.commit()

    async def remove_ubot(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ubot WHERE user_id = ?", (user_id,))
        conn.commit()

    async def get_userbots(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, ubot_data FROM ubot")
        results = cursor.fetchall()
        data = []
        for row in results:
            # row is sqlite3.Row: index 0 user_id, index 1 ubot_data
            user_id = row[0]
            encoded = row[1]
            if not encoded:
                ubot_data = {}
            else:
                decrypted = self._decrypt(encoded)
                try:
                    ubot_data = json.loads(decrypted) if decrypted else {}
                except:
                    ubot_data = {}
            data.append({
                "name": str(user_id),
                "api_id": ubot_data.get("api_id"),
                "api_hash": ubot_data.get("api_hash"),
                "session_string": ubot_data.get("session_string"),
            })
        return data

    # ----------------- prefixes -----------------
    async def get_pref(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM prefixes WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            data = self._read_json_from_col(result) or {}
            return data.get("prefixesi", ".")
        else:
            return "."

    async def set_pref(self, user_id, prefix):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM prefixes WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
        else:
            data = {}
        data["prefixesi"] = prefix
        self._write_json_to_col(cursor, "prefixes", user_id, "user_data", data)
        conn.commit()

    async def rem_pref(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM prefixes WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
            if "prefixesi" in data:
                del data["prefixesi"]
                self._write_json_to_col(cursor, "prefixes", user_id, "user_data", data)
                conn.commit()

    # ----------------- twofactor -----------------
    async def get_two_factor(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM twofactor WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            data = self._read_json_from_col(result) or {}
            return data.get("twofactor")
        else:
            return None

    async def set_two_factor(self, user_id, twofactor):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM twofactor WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
        else:
            data = {}
        data["twofactor"] = twofactor
        self._write_json_to_col(cursor, "twofactor", user_id, "user_data", data)
        conn.commit()

    async def rem_two_factor(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM twofactor WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
            if "twofactor" in data:
                del data["twofactor"]
                self._write_json_to_col(cursor, "twofactor", user_id, "user_data", data)
                conn.commit()

    # ----------------- users / expire date -----------------
    async def get_expired_date(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result:
            data = self._read_json_from_col(result) or {}
            expire_date_str = data.get("expire_date")
            if expire_date_str:
                try:
                    jkt_timezone = pytz.timezone("Asia/Jakarta")
                    expired_date = dateutil.parser.parse(expire_date_str)
                    if expired_date.tzinfo is None:
                        expired_date = jkt_timezone.localize(expired_date)
                    else:
                        expired_date = expired_date.astimezone(jkt_timezone)
                    return expired_date
                except Exception:
                    return None
            else:
                return None
        else:
            return None

    async def set_expired_date(self, user_id, expire_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM users WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
        else:
            data = {}
        if expire_date.tzinfo is None:
            local_timezone = pytz.timezone("Asia/Jakarta")
            expire_date = local_timezone.localize(expire_date)
        data["expire_date"] = expire_date.isoformat()
        self._write_json_to_col(cursor, "users", user_id, "user_data", data)
        conn.commit()

    async def rem_expired_date(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_data FROM users WHERE user_id = ?", (user_id,))
        existing = cursor.fetchone()
        if existing:
            data = self._read_json_from_col(existing) or {}
            if "expire_date" in data:
                del data["expire_date"]
            self._write_json_to_col(cursor, "users", user_id, "user_data", data)
            conn.commit()


db = DatabaseUsu(DATABASE)




