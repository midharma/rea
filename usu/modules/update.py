"""from usu import *
from usu.core.helpers._cmd import *
import subprocess
import importlib
import sys
import os

repo_dir = os.path.dirname(os.path.abspath(__file__))

@USU.BOT("update")
@USU.DEVS
async def update_code(client, message):
    try:
        pull_result = subprocess.run(['git', 'pull'], capture_output=True, text=True, check=True)
        await message.reply(f"<b><i>Output Git Pull:</i></b>\n<pre>{pull_result.stdout}</pre>")

        reloaded_modules = []
        for module_name, module_obj in list(sys.modules.items()):
            try:
                module_file = getattr(module_obj, '__file__', None)
                if module_file and module_file.startswith(repo_dir) and isinstance(module_obj, type(sys)):
                    importlib.reload(module_obj)
                    reloaded_modules.append(module_name)
            except Exception as e:
                await message.reply(f"<b><i>Gagal memuat ulang modul {module_name}: {e}</i></b>")

        if reloaded_modules:
            await message.reply(f"<b><i>Kode berhasil diupdate dan modul berikut direload:</i></b>\n<pre>{', '.join(reloaded_modules)}</pre>")
        else:
            await message.reply("<b><i>Kode berhasil diupdate, namun tidak ada modul yang relevan yang perlu direload.</i></b>")

    except subprocess.CalledProcessError as e:
        await message.reply(f"<b><i>Error saat melakukan Git pull:</i></b> {e.stderr}")
    except Exception as e:
        await message.reply(f"<b><i>Terjadi error:</i></b> {e}")"""
