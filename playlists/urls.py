from django.urls import path
from .views import (
    PlaylistListAPIView,
    PlaylistDetailAPIView,
    AddPlaylistItemAPIView,
    DeletePlaylistItemAPIView,
    generate_share_link,
    get_shared_playlist,
)

urlpatterns = [
    path('playlists/', PlaylistListAPIView.as_view()),
    path('playlists/<uuid:pk>/', PlaylistDetailAPIView.as_view()),
    path('playlist-items/add/', AddPlaylistItemAPIView.as_view()),
    path('playlist-items/<int:item_id>/delete/', DeletePlaylistItemAPIView.as_view()),
    #Share link routes:
    path('playlists/<uuid:playlist_id>/share/', generate_share_link),
    path('playlists/shared/<str:token>/', get_shared_playlist), 
]