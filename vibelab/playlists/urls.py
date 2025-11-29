from django.urls import path
from .views import (
    PlaylistListAPIView,
    PlaylistDetailAPIView,
    AddPlaylistItemAPIView,
    DeletePlaylistItemAPIView,
    generate_share_link,
    get_shared_playlist,
)
from playlists.views import generate_share_link, get_shared_playlist
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', PlaylistListAPIView.as_view()),
    path('<uuid:pk>/', PlaylistDetailAPIView.as_view()),
    path('playlist-items/add/', AddPlaylistItemAPIView.as_view()),
    path('playlist-items/<uuid:item_id>/delete/', DeletePlaylistItemAPIView.as_view()),
    #Share link routes:
    path('<uuid:playlist_id>/share/', generate_share_link),
    path('shared/<str:token>/', get_shared_playlist), 
]