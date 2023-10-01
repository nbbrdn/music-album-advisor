from django.db import models
from django.utils.html import mark_safe


class MusicAlbum(models.Model):
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updated_at = models.DateTimeField("Updated", auto_now=True)
    title = models.CharField("Title", max_length=250)
    artist = models.CharField("Artist", max_length=250)
    year = models.SmallIntegerField("Year")
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    wiki_url = models.URLField("Wikipedia", null=True, blank=True)
    spotify_url = models.URLField("Spotify", null=True, blank=True)
    apple_url = models.URLField("Apple Music", null=True, blank=True)
    youtube_url = models.URLField("YouTube", null=True, blank=True)
    yandex_url = models.URLField("Yandex Music", null=True, blank=True)

    @property
    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe(
                f'<img src="{self.thumbnail.url}" width="200" height="200" />'
            )

    def __str__(self) -> str:
        return f"{self.title}, {self.artist}"

    class Meta:
        ordering = ["-created_at"]
