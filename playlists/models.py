
import uuid
import secrets
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Playlist(models.Model):
    class VibeChoices(models.TextChoices):
        POP = "POP", "Pop"
        ROCK = "ROCK", "Rock"
        LATIN = "LATIN", "Latin"
        COUNTRY = "COUNTRY", "Country"
        TECHNO = "TECHNO", "Techno"
        RNBSOUL = "RNB/SOUL", "R&B/Soul"  # fixed HTML entity

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # allow blank for nicer forms/dev
    vibe = models.CharField(max_length=10, choices=VibeChoices.choices, default=VibeChoices.POP)
    is_open = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    # private code for locked playlists
    accessCode = models.CharField(max_length=20, blank=True, null=True)

    # token used for sharing
    share_token = models.CharField(max_length=50, blank=True, null=True, unique=True)

    # Owner (ForeignKey to your CustomUser). We'll make it nullable first to avoid the migration prompt.
    owner = models.ForeignKey(User, related_name="playlists", on_delete=models.CASCADE, blank=True, null=True)

    def generate_share_token(self):
        """Use this method when user clicks 'Share'."""
        self.share_token = secrets.token_urlsafe(16)
        self.save()

    def __str__(self):
        return self.name


class Song(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=100, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"


class PlayListItem(models.Model):
    playlist = models.ForeignKey(Playlist, related_name="items", on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name="playlist_items", on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Consider migrating to UniqueConstraint in the future
        unique_together = ("playlist", "song")

    def __str__(self):
        return f"{self.song.title} in {self.playlist.name}"
