import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types.input_file import InputFile
from dotenv import load_dotenv

from app.keyboards import main_keyboard, generate_album_keyboard
from app.controllers import (
    get_random_album,
    register_user,
    register_user_activity,
    log_bot_stop,
    count_users,
    count_albums,
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Bot has been started.')


@dp.message_handler(commands=['help'])
async def proc_cmd_help(message: types.Message):
    await message.answer(
        text=(
            'The bot gives you a random album from the '
            '"1001 Albums You Must Hear Before You Die" list.'
        ),
        reply_markup=main_keyboard,
    )
    await message.delete()


@dp.message_handler(commands=['stat'])
async def proc_cmd_stat(message: types.Message):
    users_cnt = count_users()
    albums_cnt = count_albums()
    await message.answer(text=f'Users: {users_cnt}\nAlbums: {albums_cnt}')
    await message.delete()


@dp.message_handler(commands=['start'])
async def proc_cmd_start(message: types.Message):
    register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.language_code,
    )

    await message.answer(
        text='Welcome to the music album advisor! 🎧',
        reply_markup=main_keyboard,
    )
    await message.delete()


@dp.message_handler(commands=['stop'])
async def proc_cmd_stop(message: types.Message):
    log_bot_stop(message.from_user.id)
    await message.answer(text='We will miss you too much!')
    await message.delete()


@dp.message_handler(Text(equals='Surprise Me!'))
async def proc_txt_random_album(message: types.Message):
    register_user_activity(message.from_user)

    album = get_random_album()
    if not album:
        await message.answer(text='Can not find any album 😭')
    try:
        cover = InputFile(f'media/covers/{album.cover}')
    except Exception as e:
        print(e)
        cover = InputFile('app/img/404-error.webp')

    # id_photo = await bot.send_photo(
    title = album.title
    artist = album.artist
    year = album.year
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=cover,
        caption=f'<b>{title}</b> by {artist}, <em>{year}</em>',
        parse_mode='HTML',
        reply_markup=generate_album_keyboard(
            wiki_url=album.wiki,
            spotify_url=album.spotify_url,
            apple_url=album.apple_url,
            youtube_url=album.youtube_url,
        ),
    )
    # id = id_photo['photo'][0]['file_id']
    # print(f'DBG:: id={id}')
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=on_startup
    )
