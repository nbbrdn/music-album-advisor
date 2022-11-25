import datetime
import psycopg2

from .models import MusicAlbum

dsn = {
    'dbname': 'advisor',
    'user': 'advisor',
    'password': 'advisor',
    'host': 'db',
    'port': 5432,
    'options': '-c search_path=content',
}


def generate_spotify_url(uri):
    """
    spotify:album:7yQtjAjhtNi76KRu05XWFS
    spotify_url='https://open.spotify.com/album/7yqtjajhtni76kru05xwfs',
    """
    id = uri.split(':')[-1].lower()
    return f'https://open.spotify.com/album/{id}'


def reactivate_user(user_id):
    with psycopg2.connect(**dsn) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM advisor.public.users
            WHERE telegram_id = %s AND is_active = 'yes'
            """,
            (user_id,),
        ),
        if cursor.fetchone()[0] > 0:
            cursor.execute(
                """
                UPDATE advisor.public.users
                SET is_active = 1, restart_date = %s
                WHERE telegram_id = %s
                """,
                (datetime.datetime.now(), user_id),
            )
            conn.commit()


def register_user(
    id,
    username='unknown',
    first_name='unknown',
    last_name='unknown',
    lang_code='na',
):

    with psycopg2.connect(**dsn) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM advisor.public.users
            WHERE telegram_id = %s
            """,
            (id,),
        )

        if cursor.fetchone()[0] > 0:
            reactivate_user(id)
        else:
            cursor.execute(
                """
                INSERT INTO advisor.public.users(
                    telegram_id, user_name, first_name, last_name,
                    language_code, register_date
                ) VALUES (%s, %s, %s, %s, %s, %s)
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
            conn.commit()


def log_bot_stop(user_id):
    with psycopg2.connect(**dsn) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE advisor.public.users
            SET is_active = 'false', stop_date = %s
            WHERE telegram_id = %s
            """,
            (datetime.datetime.now(), user_id),
        )
        conn.commit()


def register_user_activity(user):
    with psycopg2.connect(**dsn) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM advisor.public.users
            WHERE telegram_id = %s
            """,
            (user.id,),
        )
        if cursor.fetchone()[0] == 0:
            register_user(
                user.id,
                user.username,
                user.first_name,
                user.last_name,
                user.language_code,
            )

        cursor.execute(
            """
            UPDATE advisor.public.users
            SET last_activity_date = %s
            WHERE telegram_id = %s
            """,
            (datetime.datetime.now(), user.id),
        )
        conn.commit()


def get_random_album():
    with psycopg2.connect(**dsn) as conn, conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT *
            FROM advisor.public.albums
            ORDER BY RANDOM()
            LIMIT 1
            """
        )
        raw_data = cursor.fetchone()

        album = MusicAlbum(
            artist=raw_data[1],
            title=raw_data[2],
            year=raw_data[3],
            cover=raw_data[4] + '.jpg',
            wiki=raw_data[5],
            spotify_url=generate_spotify_url(raw_data[7]),
            apple_url=raw_data[8],
            youtube_url=raw_data[9],
        )

        return album
