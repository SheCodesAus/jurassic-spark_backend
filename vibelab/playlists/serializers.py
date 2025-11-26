from rest_framework import serializers
from .models import Playlist, Song, PlayListItem




# --- Song Serializer ---
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'album', 'spotify_id', 'added_at']



# --- Playlist Item Serializer (nested song) ---
class PlayListItemSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)

    class Meta:
        model = PlayListItem
        fields = '__all__'



# --- Playlist Serializer (with nested playlist items) ---
class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    items = PlayListItemSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'




# --- Add Song to Playlist Serializer ---
# This one is used when a user POSTS a song to playlist
class AddPlayListItemSerializer(serializers.Serializer):
    spotify_id = serializers.CharField()

    def validate(self, data):
        if not data.get("spotify_id"):
            raise serializers.ValidationError("spotify_id is required.")
        return data



class AddSongSerializer(serializers.Serializer):
    playlist_id = serializers.UUIDField()
    spotify_id = serializers.CharField()
    title = serializers.CharField()
    artist = serializers.CharField()
    album = serializers.CharField()