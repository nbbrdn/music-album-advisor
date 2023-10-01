from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

random_album_button = KeyboardButton(text="😲 Surprise Me!")
main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[[random_album_button]]
)


def generate_album_keyboard(wiki_url, spotify_url, apple_url, youtube_url):
    album_keyboard = InlineKeyboardMarkup(row_width=2)
    spotify_button = InlineKeyboardButton("Spotify", url=spotify_url)
    apple_button = InlineKeyboardButton("Apple Music", url=apple_url)
    youtube_button = InlineKeyboardButton(
        text="YouTube",
        url=youtube_url,
    )

    album_keyboard.add(spotify_button, apple_button).add(youtube_button)

    return album_keyboard
