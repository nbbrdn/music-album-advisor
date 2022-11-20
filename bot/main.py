from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types.input_file import InputFile

from config import TELEGRAM_TOKEN
from keyboards import main_keyboard, generate_album_keyboard
from controllers import get_random_album, register_user

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Bot has been started.')


@dp.message_handler(commands=['start'])
async def proc_cmd_start(message: types.Message):
    register_user(message.from_user.id, message.from_user.first_name)
    await message.answer(
        text='Welcome to the music album advisor! 🎧',
        reply_markup=main_keyboard,
    )
    await message.delete()


@dp.message_handler(Text(equals='Surprise Me!'))
async def proc_txt_random_album(message: types.Message):
    album = get_random_album()
    cover = InputFile(f'media/{album.cover}')

    id_photo = await bot.send_photo(
        chat_id=message.chat.id,
        photo=cover,
        caption=f'<b>{album.title}</b> by {album.artist}, <em>{album.year}</em>',
        parse_mode='HTML',
        reply_markup=generate_album_keyboard(
            wiki_url=album.wiki,
            spotify_url=album.spotify_url,
            apple_url=album.apple_url,
            youtube_url=album.youtube_url,
        ),
    )
    id = id_photo['photo'][0]['file_id']
    print(f'DBG:: id={id}')
    await message.delete()


if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=on_startup
    )
