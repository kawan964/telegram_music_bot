# -----------------------
# telegram_music_bot_full.py
# -----------------------

import os
import zipfile

# =========================
# 1️⃣ فایلەکان داخلی (in-memory)
# =========================

files_content = {
    "main.py": """from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import InputStream, AudioPiped
import yt_dlp
import os

API_ID = int(os.environ.get("23487033"))
API_HASH = os.environ.get("d2135b359e73aff29b3734dc7ce5d487")
BOT_TOKEN = os.environ.get("8235918813:AAEk9uT55WnaVjuBLogs9wX31OBQLJmsBY8")

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        await message.reply("🎵 ناوی گۆرانی بنوسە: `/play despacito`")
        return
    query = " ".join(message.command[1:])
    await message.reply(f"🔍 گەڕان بۆ گۆرانی: {query}")
    
    ydl_opts = {"format": "bestaudio/best", "noplaylist": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        url = info["entries"][0]["url"]
    
    chat_id = message.chat.id
    await call_py.join_group_call(chat_id, InputStream(AudioPiped(url)))
    await message.reply("▶️ گۆرانی دەستپێکرد!")

@app.on_message(filters.command("song") & filters.private)
async def song(_, message):
    if len(message.command) < 2:
        await message.reply("🎶 ناوی گۆرانی بنوسە: `/song despacito`")
        return
    query = " ".join(message.command[1:])
    await message.reply(f"🔍 گەڕان بۆ گۆرانی: {query}")
    
    ydl_opts = {"format": "bestaudio/best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_name = ydl.prepare_filename(info["entries"][0])
    
    await message.reply_audio(file_name)
    os.remove(file_name)

call_py.start()
app.start()
idle()
""",
    "requirements.txt": """pyrogram==2.0.106
pytgcalls==0.9.5
yt-dlp
tgcrypto
""",
    "Procfile": "worker: python3 main.py\n",
    "runtime.txt": "python-3.10.12\n"
}

# =========================
# 2️⃣ دروستکردنی ZIP
# =========================

zip_path = "telegram_music_bot_full.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for filename, content in files_content.items():
        zipf.writestr(filename, content)

print(f"✅ فایل ZIP دروست کرا: {zip_path}")
print("ئێستا دەتوانیت فایل ZIP باربکەیت لە GitHub و Deploy بکەیت لە Railway")