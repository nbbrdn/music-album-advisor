from django.contrib import admin
from django.utils.html import format_html

from .models import MusicAlbum, StreamingService, AlbumStreaming


class AlbumStreamings(admin.StackedInline):
    model = AlbumStreaming
    extra = 0


@admin.register(StreamingService)
class StreamServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(MusicAlbum)
class MusicAlbumAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year", "artist")
    list_display_links = ("title",)
    readonly_fields = ("thumbnail_preview",)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = "Thumbnail Preview"
    thumbnail_preview.allow_tags = True

    inlines = (AlbumStreamings,)
