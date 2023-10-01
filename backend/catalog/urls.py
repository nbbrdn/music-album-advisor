from django.urls import path
from . import views


urlpatterns = [path("random_album/", views.random_music_album, name="random_album")]
