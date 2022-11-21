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


def reactivate_user(user_id):
    con = sqlite3.connect('albums.db')
    cur = con.cursor()

    cur.execute(
        f"SELECT Count() FROM users WHERE user_id = '{user_id}' AND is_active = 0"
    )
    if cur.fetchone()[0] > 0:
        cur.execute(
            """
            UPDATE users SET is_active = 1, restart_date = ? WHERE user_id = ?
            """,
            (datetime.datetime.now(), user_id),
        )
        con.commit()
    con.close()


def register_user(
    id, username, first_name=None, last_name=None, lang_code=None
):
    con = sqlite3.connect('albums.db')
    cur = con.cursor()

    cur.execute(f"SELECT Count() FROM users WHERE user_id = '{id}'")
    if cur.fetchone()[0] > 0:
        con.close()
        reactivate_user(id)
        return

    cur.execute(
        """
            INSERT INTO users(
                user_id, user_name, first_name, last_name,
                language_code, join_date
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
        (
            id,
            username,
            first_name,
            last_name,
            lang_code,
            datetime.datetime.now(),
        ),
    )
    con.commit()
    con.close()


def log_bot_stop(user_id):
    con = sqlite3.connect('albums.db')
    cur = con.cursor()

    cur.execute(
        """
        UPDATE users SET is_active = 0, stop_date = ? WHERE user_id = ?
        """,
        (datetime.datetime.now(), user_id),
    )

    con.commit()
    con.close()


def register_user_activity(user_id):
    con = sqlite3.connect('albums.db')
    cur = con.cursor()

    cur.execute(f"SELECT Count() FROM users WHERE user_id = '{user_id}'")
    if cur.fetchone()[0] == 0:
        register_user(user_id)

    cur.execute(
        """
        UPDATE users SET last_activity_date = ? WHERE user_id = ?
        """,
        (datetime.datetime.now(), user_id),
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
