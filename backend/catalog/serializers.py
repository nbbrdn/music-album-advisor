from rest_framework import serializers
from .models import MusicAlbum, AlbumStreaming


class AlbumStreamingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumStreaming
        fields = (
            "url",
            "streaming_service",
        )


class MusicAlbumSerializer(serializers.ModelSerializer):
    streams = AlbumStreamingSerializer(many=True, read_only=True)

    class Meta:
        model = MusicAlbum
        fields = ("pk", "title", "artist", "year", "thumbnail", "streams")
