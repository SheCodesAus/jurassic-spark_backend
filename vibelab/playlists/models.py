import uuid
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class Playlist(models.Model):
    class VibeChoices(models.TextChoices):
        POP = 'POP', 'Pop'
        ROCK = 'ROCK', 'Rock'
        LATIN = 'LATIN', 'Latin'
        COUNTRY = 'COUNTRY', 'Country'
        TECHNO = 'TECHNO', 'Techno'
        RNBSOUL = 'RNB/SOUL', 'R&B/Soul'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    name = models.CharField(max_length=200)
    description = models.TextField()
    vibe = models.CharField(max_length=10, choices=VibeChoices.choices, default=VibeChoices.POP)
    is_open = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    accessCode = models.CharField(max_length=20, blank=True, null=True)

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
    playlist = models.ForeignKey(Playlist, related_name='items', on_delete=models.CASCADE)
    song = models.ForeignKey(Song, related_name='playlist_items', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'song')

    def __str__(self):
        return f"{self.song.title} in {self.playlist.name}"