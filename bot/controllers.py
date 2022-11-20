import datetime
import sqlite3

from models import MusicAlbum


def generate_spotify_url(uri):
    """
    spotify:album:7yQtjAjhtNi76KRu05XWFS
    spotify_url='https://open.spotify.com/album/7yqtjajhtni76kru05xwfs',
    """
    id = uri.split(':')[-1].lower()
    return f'https://open.spotify.com/album/{id}'


def register_user(user_id, user_first_name):
    con = sqlite3.connect('albums.db')
    cur = con.cursor()

    cur.execute(f"SELECT Count() FROM users WHERE user_id = '{user_id}'")
    if cur.fetchone()[0] > 0:
        con.close()
        return

    cur.execute(
        """
            INSERT INTO users(
                user_id, user_name, join_date
            ) VALUES (?, ?, ?)
            """,
        (user_id, user_first_name, datetime.datetime.now()),
    )
    con.commit()

    con.close()


def get_random_album():
    con = sqlite3.connect('albums.db')
    cur = con.cursor()

    res = cur.execute('SELECT * FROM albums ORDER BY RANDOM() LIMIT 1')
    raw_data = res.fetchone()

    con.close()

    album = MusicAlbum(
        title=raw_data[1],
        artist=raw_data[0],
        year=raw_data[2],
        wiki=raw_data[5],
        spotify_url=generate_spotify_url(raw_data[6]),
        apple_url=raw_data[7],
        youtube_url=raw_data[8],
        cover=raw_data[3] + '.jpg',
    )

    return album
