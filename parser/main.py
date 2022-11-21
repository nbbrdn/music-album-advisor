import requests
import shutil
import sqlite3

from bs4 import BeautifulSoup


def parse_page(url: str, apple_url: str = None):
    album = {}
    raw_html = requests.get(url)
    soup = BeautifulSoup(raw_html.content, 'html.parser')
    album['title'] = soup.find('h1').text.strip().replace("'", "''")
    album['artist'] = soup.find_all('h2')[0].text.strip().replace("'", "''")
    album['year'] = soup.find_all('h2')[-1].text.strip()

    album['wikipedia_url'] = soup.find('a', text='Wikipedia')['href']

    description_div = soup.find_all(
        'div', class_='static-album--description--column'
    )[1]
    description = description_div.find('p').text.strip().replace("'", "''")
    album['description'] = description

    streaming_div = soup.find('div', class_='streaming-wrapper')
    streaming_urls = streaming_div.find_all('a')
    for anchor in streaming_urls:
        ref = anchor['href']
        if 'spotify' in ref:
            album['spotify_url'] = ref
        elif 'youtube' in ref:
            album['youtube_url'] = ref
        elif 'apple' in ref:
            album['apple_url'] = ref
        else:
            album['other_url'] = ref

    cover_url = soup.find('img', class_='album-cover-img')['src']
    album['file_name'] = cover_url.split('/')[-1]
    file_name_full = album['file_name'] + '.jpg'

    res = requests.get(cover_url, stream=True)
    if res.status_code == 200:
        with open(f'media/{file_name_full}', 'wb') as f:
            shutil.copyfileobj(res.raw, f)

    if 'apple' not in album and apple_url:
        album['apple_url'] = apple_url

    return album


def prepare_db():
    con = sqlite3.connect('albums.db')
    cur = con.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS albums(
            artist TEXT NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOU NULL,
            cover TEXT,
            description TEXT,
            wiki_url TEXT,
            spotify_url TEXT,
            apple_url TEXT,
            youtube_url TEXT,
            other_url TEXT
        )
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS urls(
            url TEXT,
            done INTEGER DEFAULT(0)
        )
        """
    )

    return con


def save_album(album, con):
    cur = con.cursor()

    artist = album['artist']
    title = album['title']
    year = album['year']

    try:
        cur.execute(
            f"SELECT Count() FROM albums WHERE artist = '{artist}' AND title = '{title}' AND year = {year}"
        )
        if cur.fetchone()[0] > 0:
            return 'duplicate'

        cur.execute(
            """
            INSERT INTO albums(
                artist, title, year, cover, wiki_url,
                spotify_url, apple_url, youtube_url, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                artist,
                title,
                year,
                album['file_name'],
                album['wikipedia_url'],
                album['spotify_url'],
                album['apple_url'],
                album['youtube_url'],
                album['description'],
            ),
        )

        con.commit()
        return 'success'
    except Exception as e:
        return f'error: {e}\n\ndata: {album}\n\n\n\n'


def fetch_album_urls(con):
    cur = con.cursor()

    raw_html = requests.get('https://1001albumsgenerator.com/')
    soup = BeautifulSoup(raw_html.content, 'html.parser')
    all_albums_div = soup.find('ul', class_='list-unstyled')
    albums = all_albums_div.find_all('a')

    for album in albums:
        url = album['href']

        cur.execute(f"SELECT Count() FROM urls WHERE url = '{url}'")
        if cur.fetchone()[0] > 0:
            next

        cur.execute(
            """
            INSERT INTO urls(url, done) VALUES (?, ?)
            """,
            (url, 0),
        )
        con.commit()


def proc_album_list(con, limit=1):
    cur = con.cursor()
    res = cur.execute(
        f"SELECT url, apple FROM urls WHERE done = 0 LIMIT {limit}"
    )
    for el in res.fetchall():
        url = el[0]
        apple_url = el[1]
        full_url = f'https://1001albumsgenerator.com{url}'
        album = parse_page(full_url, apple_url)

        if album and 'apple_url' in album:
            result = save_album(album, con)
            if result in ('success', 'duplicate'):
                cur.execute(f"UPDATE urls SET done = 1 WHERE url = '{url}'")
                con.commit()
            else:
                print(result)
        else:
            print("Can't find an Apple URL")
            print(album)


def main():
    con = prepare_db()
    proc_album_list(con, limit=500)
    con.close()


if __name__ == '__main__':
    main()
