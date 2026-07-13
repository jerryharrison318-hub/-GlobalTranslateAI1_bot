import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing.")


bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):

    keyboard = InlineKeyboardBuilder()

    keyboard.button(text="🌍 Translate", callback_data="translate")
    keyboard.button(text="📚 Languages", callback_data="languages")
    keyboard.button(text="ℹ️ About", callback_data="about")
    keyboard.button(text="❓ Help", callback_data="help")

    keyboard.adjust(2)

    await message.answer(
        """
🌍 <b>Welcome to GlobalTranslateBot</b>

Translate text instantly into over 100 languages.

Perfect for:

🎓 Students
✈️ Travelers
💼 Businesses
🌎 Everyday Conversations

Select an option below to begin.
""",
        reply_markup=keyboard.as_markup()
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
