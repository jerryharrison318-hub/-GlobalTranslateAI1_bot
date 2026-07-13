import os
import aiohttp
import asyncio
import logging

API_URL = os.getenv(
    "TRANSLATE_API",
    "https://translate.argosopentech.com/translate"
)

HEADERS = {
    "Content-Type": "application/json"
}


async def translate(text: str, target: str):

    payload = {
        "q": text,
        "source": "auto",
        "target": target,
        "format": "text"
    }

    timeout = aiohttp.ClientTimeout(total=30)

    try:

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.post(
                API_URL,
                json=payload,
                headers=HEADERS,
            ) as response:

                if response.status != 200:

                    logging.error(
                        f"Translation API Error: {response.status}"
                    )

                    return None

                data = await response.json()

                if "translatedText" not in data:
                    return None

                return data["translatedText"]

    except asyncio.TimeoutError:

        logging.error("Translation timeout.")

        return None

    except Exception as e:

        logging.exception(e)

        return None
