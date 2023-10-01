from rest_framework import serializers
from .models import MusicAlbum


class MusicAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicAlbum
        fields = ("pk", "title", "artist", "year", "thumbnail", "yandex_url")
