import random

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MusicAlbum
from .serializers import MusicAlbumSerializer


@api_view(["GET"])
def random_music_album(request):
    albums = list(MusicAlbum.objects.all())
    random_album = random.sample(albums, 1)[0]
    serializer = MusicAlbumSerializer(random_album)
    return Response(serializer.data)
