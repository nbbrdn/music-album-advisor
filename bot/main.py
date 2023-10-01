import asyncio
import os
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from app.keyboards import main_keyboard

TOKEN = os.getenv("TELEGRAM_TOKEN", "")
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Hello, {hbold(message.from_user.full_name)}!\nWelcome to the Music Album Advisor! 🎧",
        reply_markup=main_keyboard,
    )
    await message.delete()


@dp.message(Command("stop"))
async def proc_cmd_stop(message: Message):
    await message.answer(text="We will miss you too much!")
    await message.delete()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
