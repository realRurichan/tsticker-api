import aiohttp
import urllib.parse
from PIL import Image
import io


class TelegramBotTokenError(Exception):
    def __init__(self, message):
        self.message = message


class Bot:
    def __init__(self, token: str):
        self.token = token
        if self.token == None:
            raise TelegramBotTokenError("No Telegram Bot Token")
        self.api = f"https://api.telegram.org/bot{self.token}/"

    async def initialize(self):
        verify = await self.doAPIReq("getMe", {})
        if verify is not None and verify["ok"]:
            pass
        else:
            raise TelegramBotTokenError("Invalid token.")

    async def fetch(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def doAPIReq(self, func: str, params: dict):
        req = f"{self.api}{func}?{urllib.parse.urlencode(params)}"
        return await self.fetch(req)

    async def downloadFile(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.read()
                return data

    def convertImageFormat(self, image_input, image_output):
        with io.BytesIO(image_input) as image_input:
            with Image.open(image_input) as img:
                img.save(image_output)

    async def getSticker(self, file_id: str, filename: str):
        res = await self.doAPIReq("getFile", {"file_id": file_id})
        if res is not None and res["ok"]:
            pass
        else:
            error = {
                "code": res["error_code"],
                "description": res["description"],
            }
            return error
        res = res["result"]
        sticker_link = (
            f"https://api.telegram.org/file/bot{self.token}/{res['file_path']}"
        )
        sticker = await self.downloadFile(sticker_link)
        dictionary = f"stickers/{filename}"
        self.convertImageFormat(sticker, dictionary)
        return True
