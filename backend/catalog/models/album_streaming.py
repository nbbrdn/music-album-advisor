from django.db import models


class AlbumStreaming(models.Model):
    album = models.ForeignKey("MusicAlbum", on_delete=models.CASCADE)
    streaming_service = models.ForeignKey("StreamingService", on_delete=models.CASCADE)
    url = models.URLField("Album URL")

    def __str__(self):
        return self.streaming_service.name
