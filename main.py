import os
import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN is missing!")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

user_language = {}

# -------------------- START --------------------

@dp.message(CommandStart())
async def start(message: Message):

    kb = InlineKeyboardBuilder()

    kb.button(text="🌍 Translate", callback_data="translate")
    kb.button(text="📚 Languages", callback_data="languages")
    kb.button(text="ℹ️ About", callback_data="about")
    kb.button(text="❓ Help", callback_data="help")

    kb.adjust(2)

    await message.answer(
        """
🌍 <b>GlobalTranslate AI</b>

Translate text into over 100+ languages.

Perfect for:

🎓 Students
✈️ Travelers
💼 Business
🌎 Everyday Conversation

Choose an option below.
""",
        reply_markup=kb.as_markup()
    )

# -------------------- BUTTONS --------------------

@dp.callback_query(F.data == "translate")
async def translate(callback: CallbackQuery):

    user_language[callback.from_user.id] = True

    await callback.message.answer(
        "✍️ Send me the text you want to translate."
    )

    await callback.answer()


@dp.callback_query(F.data == "languages")
async def languages(callback: CallbackQuery):

    await callback.message.answer(
        """
🌍 Supported Languages

🇺🇸 English
🇪🇸 Spanish
🇫🇷 French
🇩🇪 German
🇮🇹 Italian
🇯🇵 Japanese
🇰🇷 Korean
🇨🇳 Chinese
🇷🇺 Russian

...and many more.
"""
    )

    await callback.answer()


@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):

    await callback.message.answer(
        """
🌍 <b>GlobalTranslate AI</b>

Fast, simple and free language translation directly inside Telegram.
"""
    )

    await callback.answer()


@dp.callback_query(F.data == "help")
async def help(callback: CallbackQuery):

    await callback.message.answer(
        """
How to use:

1️⃣ Click Translate

2️⃣ Send your text

3️⃣ Choose a language

4️⃣ Receive your translation
"""
    )

    await callback.answer()


# -------------------- USER MESSAGE --------------------

@dp.message()
async def receive_text(message: Message):

    if user_language.get(message.from_user.id):

        user_language[message.from_user.id] = False

        await message.answer(
            f"""
Detected Text:

<code>{message.text}</code>

✅ Great!

Translation API will process this in the next update.
"""
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
