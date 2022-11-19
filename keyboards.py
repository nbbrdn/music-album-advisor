from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
random_album_button = KeyboardButton(text='Surprise Me!')
main_keyboard.add(random_album_button)

album_keyboard = InlineKeyboardMarkup(row_width=2)
spotify_button = InlineKeyboardButton(
    'Spotify', url='https://open.spotify.com/album/4CGGf13zt9Jva2ia4CKQi6'
)
apple_button = InlineKeyboardButton(
    'Apple Music', url='https://music.apple.com/album/682197269'
)
youtube_button = InlineKeyboardButton(
    text='YouTube',
    url='https://www.youtube.com/results?search_query=Zombie%20-%20Fela%20Kuti',
)

album_keyboard.add(spotify_button, apple_button).add(youtube_button)
