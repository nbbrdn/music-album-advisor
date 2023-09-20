from django.db import models


class MusicAlbum(models.Model):
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updated_at = models.DateTimeField("Updated", auto_now=True)
    title = models.CharField("Title", max_length=250)
    artist = models.CharField("Artist", max_length=250)
    year = models.SmallIntegerField("Year")
    wiki_url = models.URLField("Wikipedia", null=True)
    spotify_url = models.URLField("Spotify", null=True)
    apple_url = models.URLField("Apple Music", null=True)
    youtube_url = models.URLField("YouTube", null=True)
    yandex_url = models.URLField("Yandex Music", null=True)

    class Meta:
        ordering = ["-created_at"]
