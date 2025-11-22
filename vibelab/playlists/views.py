from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from playlists.models import Playlist, PlayListItem, Song
from playlists.serializers import (
    PlaylistSerializer,
    PlayListItemSerializer,
    AddSongSerializer,
)


# --------------------------------------------------
# Custom Permissions
# --------------------------------------------------

class HasPlaylistAccess(permissions.BasePermission):
    """
    User must:
    - be the owner OR
    - provide correct accessCode (in header or request.data)
    - at frontend, we can store the accessCode in localStorage or context after first access
    """

    def has_object_permission(self, request, view, playlist: Playlist):
        # 1. Owners always have full access
        if request.user.is_authenticated and playlist.owner == request.user:
                return True

        # 2. Accept accessCode from header OR request body
        provided_code = (
            request.headers.get("X-Access-Code")
            or request.data.get("accessCode")
            or request.query_params.get("accessCode")  # GET support
        )

        if provided_code and provided_code == playlist.accessCode:
            return True

        return False


class IsPlaylistOwner(permissions.BasePermission):
    """Only owner can update/delete playlist"""

    def has_object_permission(self, request, view, playlist: Playlist):
        return (
            request.user.is_authenticated
            and hasattr(playlist, "owner")
            and playlist.owner == request.user
        )


# --------------------------------------------------
# Playlist List + Create
# --------------------------------------------------

class PlaylistListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        playlists = Playlist.objects.filter(is_open=False)  # all private, but viewable only by accessCode individually
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            playlist = serializer.save(owner=request.user)  # requires owner field in Playlist model
            return Response(
                PlaylistSerializer(playlist).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------------------------------------
# Playlist Detail (requires accessCode or owner)
# --------------------------------------------------

class PlaylistDetailAPIView(APIView):
    permission_classes = [HasPlaylistAccess]

    def get(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)

        self.check_object_permissions(request, playlist)

        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)

    def put(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)

        # Only owner can update
        if not IsPlaylistOwner().has_object_permission(request, self, playlist):
            return Response({"detail": "Not allowed."}, status=403)

        serializer = PlaylistSerializer(playlist, data=request.data, partial=True)

        if serializer.is_valid():
            updated = serializer.save()
            return Response(PlaylistSerializer(updated).data)

        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        playlist = get_object_or_404(Playlist, pk=pk)

        # Only owner can delete
        if not IsPlaylistOwner().has_object_permission(request, self, playlist):
            return Response({"detail": "Not allowed."}, status=403)

        playlist.delete()
        return Response(status=204)


# --------------------------------------------------
# Add Song to Playlist (requires accessCode or owner)
# --------------------------------------------------

class AddPlaylistItemAPIView(APIView):
    permission_classes = [HasPlaylistAccess]

    def post(self, request):
        # Validate request body
        serializer = AddSongSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        playlist_id = serializer.validated_data["playlist_id"]
        playlist = get_object_or_404(Playlist, id=playlist_id)

        # Permission using custom logic
        self.check_object_permissions(request, playlist)

        spotify_id = serializer.validated_data["spotify_id"]

        # Create or reuse Song
        song, _ = Song.objects.get_or_create(
            spotify_id=spotify_id,
            defaults={
                "title": serializer.validated_data["title"],
                "artist": serializer.validated_data["artist"],
                "album": serializer.validated_data["album"],
            }
        )

        # Create playlist item
        item, _ = PlayListItem.objects.get_or_create(
            playlist=playlist,
            song=song
        )

        return Response(
            PlayListItemSerializer(item).data,
            status=status.HTTP_201_CREATED
        )



class DeletePlaylistItemAPIView(APIView):
    """
    Only playlist owner can delete a song from playlist.
    """
    permission_classes = [IsPlaylistOwner]  # must be logged in

    def delete(self, request, item_id):
        item = get_object_or_404(PlayListItem, id=item_id)
        playlist = item.playlist

        # Check owner permission
        if playlist.owner != request.user:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        item.delete()
        return Response({"detail": "Song deleted from playlist."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_share_link(request, playlist_id):
    """
    Generates a share link (token) for the playlist. Only the owner can generate the link.
    """
    playlist = get_object_or_404(Playlist, id=playlist_id, owner=request.user)
    
    # Generate a new share token
    playlist.generate_share_token()

    share_url =f"https://vibelab.netlify.app/share/{playlist.share_token}"

    return Response({"share_url": share_url})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_shared_playlist(request, token):
    """Anyone with the share token can access the playlist."""
    playlist = get_object_or_404(Playlist, share_token=token)

    serializer = PlaylistSerializer(playlist)
    return Response(serializer.data)