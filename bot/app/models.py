from dataclasses import dataclass


@dataclass
class MusicAlbum:
    title: str
    artist: str
    year: int
    wiki: str
    spotify_url: str
    apple_url: str
    youtube_url: str
    cover: str
