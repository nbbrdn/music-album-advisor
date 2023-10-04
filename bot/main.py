import asyncio
import logging
import os
import requests
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils.markdown import hbold


TOKEN = os.getenv("TELEGRAM_TOKEN", "")
dp = Dispatcher()

random_album_button = KeyboardButton(text="Surprise Me!")
main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[[random_album_button]]
)


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


@dp.message(F.text.lower() == "surprise me!")
async def proc_random_album_command(message: Message):
    try:
        headers = {"Accept": "application/json"}
        response = requests.get("http://api:8000/api/random_album/", headers=headers)
    except:
        await message.answer("Something gone wrong.")
    if response.status_code == 200:
        response_data = response.json()
        reply = response_data.get("yandex_url", "Can't get the album's url.")
        await message.answer(reply)
    else:
        await message.answer("Can not find any album 😭")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
