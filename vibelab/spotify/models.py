
from django.conf import settings
from django.db import models

class SpotifyAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="spotify_accounts")
    spotify_user_id = models.CharField(max_length=128, unique=True)
    access_token = models.TextField(blank=True, default="")
    refresh_token = models.TextField()
    token_expires_at = models.DateTimeField()
    scope = models.TextField(blank=True, default="")  # store granted scopes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} ↔ {self.spotify_user_id}"
