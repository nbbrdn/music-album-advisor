import random

from models import MusicAlbum

db = []

zombie = MusicAlbum(
    title='Zombie',
    artist='Fela Kuti',
    year=1977,
    wiki='https://en.wikipedia.org/wiki/Zombie_(album)',
    spotify_url='https://open.spotify.com/album/4CGGf13zt9Jva2ia4CKQi6',
    apple_url='https://music.apple.com/album/682197269',
    youtube_url='https://www.youtube.com/results?search_query=Zombie%20-%20Fela%20Kuti',
    cover='https://upload.wikimedia.org/wikipedia/en/f/f5/FelaZombie.jpg',
)

db.append(zombie)


def get_random_album():
    global db
    return random.choice(db)
