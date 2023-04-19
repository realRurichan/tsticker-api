from flask import Flask, send_from_directory
from bot import Bot
from dotenv import load_dotenv
import json
import re
import os

app = Flask(__name__)
load_dotenv()
bot_token = os.getenv("TOKEN")
bot = Bot(bot_token)


@app.route("/stickers/<filename>")
async def get_sticker(filename):
    await bot.initialize()
    print(filename)
    pattern = r"^[^.]+\.(jpg|jpeg|png|webp)$"
    match = re.match(pattern, filename)
    if match:
        file_id, ext = filename.split(".")
    else:
        error = {"code": "400", "description": "Bad Request: invalid filename"}
        return json.dumps(error)
    result = await bot.getSticker(file_id=file_id, filename=filename)
    if result == True:
        return send_from_directory("stickers", filename)
    else:
        return json.dumps(result)
