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
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from translator import translate
from languages import LANGUAGES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing.")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
)

dp = Dispatcher()

waiting_users = {}
pending_text = {}


def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌍 Translate",
                    callback_data="translate",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📚 Languages",
                    callback_data="languages",
                ),
                InlineKeyboardButton(
                    text="❓ Help",
                    callback_data="help",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ About",
                    callback_data="about",
                )
            ],
        ]
    )


def language_keyboard():

    rows = []

    row = []

    for code, name in LANGUAGES.items():

        row.append(
            InlineKeyboardButton(
                text=name,
                callback_data=f"lang:{code}",
            )
        )

        if len(row) == 2:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )


@dp.message(CommandStart())
async def start(message: Message):

    text = """
🌍 <b>GlobalTranslate AI</b>

Welcome!

Translate text instantly into multiple languages.

Features

✅ Auto Language Detection
✅ Fast Translation
✅ Multiple Languages
✅ Easy To Use

Choose an option below.
"""

    await message.answer(
        text,
        reply_markup=main_menu(),
    )


@dp.callback_query(F.data == "translate")
async def translate_button(callback: CallbackQuery):

    waiting_users[
        callback.from_user.id
    ] = True

    await callback.message.answer(
        "✍️ Send me the text you want to translate."
    )

    await callback.answer()


@dp.callback_query(F.data == "about")
async def about(callback: CallbackQuery):

    await callback.message.answer(
        """
🌍 <b>GlobalTranslate AI</b>

Version 1.0

A free Telegram translation assistant powered by LibreTranslate.

Created for students, travelers and businesses.
"""
    )

    await callback.answer()


@dp.callback_query(F.data == "help")
async def help_button(callback: CallbackQuery):

    await callback.message.answer(
        """
<b>How To Use</b>

1. Press 🌍 Translate

2. Send your text

3. Choose the language

4. Receive your translation
"""
    )

    await callback.answer()@dp.callback_query(F.data == "languages")
async def languages(callback: CallbackQuery):

    text = "<b>Supported Languages</b>\n\n"

    for _, language in LANGUAGES.items():
        text += f"{language}\n"

    await callback.message.answer(text)

    await callback.answer()


@dp.message()
async def receive_text(message: Message):

    user_id = message.from_user.id

    if not waiting_users.get(user_id):
        return

    waiting_users[user_id] = False

    pending_text[user_id] = message.text

    await message.answer(
        "🌍 Select the language you want to translate into:",
        reply_markup=language_keyboard(),
    )


@dp.callback_query(F.data.startswith("lang:"))
async def translate_callback(callback: CallbackQuery):

    user_id = callback.from_user.id

    if user_id not in pending_text:

        await callback.answer(
            "No text found.",
            show_alert=True,
        )

        return

    target = callback.data.split(":")[1]

    text = pending_text[user_id]

    await callback.message.edit_text(
        "⏳ Translating..."
    )

    try:

        translated = await translate(
            text=text,
            target=target,
        )

        if not translated:

            await callback.message.answer(
                "❌ Translation failed.\nPlease try again later."
            )

            await callback.answer()

            return

        language_name = LANGUAGES.get(
            target,
            target.upper(),
        )

        await callback.message.answer(
            f"""
<b>✅ Translation Complete</b>

🌍 <b>Target Language:</b>
{language_name}

📝 <b>Original Text:</b>

<code>{text}</code>

📖 <b>Translated Text:</b>

<code>{translated}</code>
""",
            reply_markup=main_menu(),
        )

        del pending_text[user_id]

    except Exception as e:

        logging.exception(e)

        await callback.message.answer(
            "❌ An unexpected error occurred."
        )

    await callback.answer()# -----------------------------
# Error Handler
# -----------------------------

@dp.error()
async def error_handler(event, exception):

    logging.exception(
        "Unhandled Error: %s",
        exception
    )

    return True


# -----------------------------
# Startup
# -----------------------------

async def on_startup():

    logging.info("===================================")
    logging.info("🌍 GlobalTranslate AI Started")
    logging.info("===================================")


# -----------------------------
# Main
# -----------------------------

async def main():

    await on_startup()

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
    )


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):

        logging.info(
            "Bot stopped."
        )
