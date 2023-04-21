from flask import Flask, send_from_directory
from bot import Bot
from dotenv import load_dotenv
import json
import re
import os
import asyncio

app = Flask(__name__)
load_dotenv()
bot_token = os.getenv("TOKEN")
cache_time = os.getenv("CACHE_TIME")
bot = Bot(bot_token)


async def delete_files():
    while True:
        await asyncio.sleep(cache_time)
        for file in os.listdir("/stickers"):
            file_path = os.path.join("/stickers", file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")


@app.route("/stickers/<filename>")
async def get_sticker(filename):
    await bot.initialize()
    pattern = r"^[^.]+\.(jpg|jpeg|png|webp)$"
    match = re.match(pattern, filename)
    if match:
        file_id, ext = filename.split(".")
    else:
        error = {"code": "400", "description": "Bad Request: invalid filename"}
        return json.dumps(error)
    file_path = f"stickers/{filename}"
    if os.path.exists(file_path):
        return send_from_directory("stickers", filename)
    result = await bot.getSticker(file_id=file_id, filename=filename)
    if result == True:
        return send_from_directory("stickers", filename)
    else:
        return json.dumps(result)
