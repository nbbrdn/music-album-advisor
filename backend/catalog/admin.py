from django.contrib import admin

from .models import MusicAlbum


@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year", "artist")
