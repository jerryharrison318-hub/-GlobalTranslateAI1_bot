import os
import aiohttp

API_URL = os.getenv("TRANSLATE_API")

async def translate(text, target):

    payload = {
        "q": text,
        "source": "auto",
        "target": target,
        "format": "text"
    }

    async with aiohttp.ClientSession() as session:

        async with session.post(API_URL, json=payload) as response:

            if response.status != 200:
                return None

            data = await response.json()

            return data.get("translatedText")
