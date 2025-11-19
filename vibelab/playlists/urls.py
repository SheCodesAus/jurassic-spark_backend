from django.urls import path
from .views import (
    PlaylistListAPIView,
    PlaylistDetailAPIView,
    AddPlaylistItemAPIView,
    DeletePlaylistItemAPIView
)

urlpatterns = [
    path('playlists/', PlaylistListAPIView.as_view()),
    path('playlists/<uuid:pk>/', PlaylistDetailAPIView.as_view()),
    path('playlist-items/add/', AddPlaylistItemAPIView.as_view()),
    path('playlist-items/<int:item_id>/delete/', DeletePlaylistItemAPIView.as_view()),
]