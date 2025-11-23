
import secrets
import string
import time
from datetime import datetime, timezone, timedelta

import requests  # using requests since you’re server-side
from django.utils import timezone as dj_tz

from vibelab.spotify.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL, TOKEN_URL, SCOPES
from vibelab.spotify.models import SpotifyAccount

def _generate_state(length=16):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def get_authorize_url(scopes=SCOPES, state=None):
    """
    Returns the Spotify authorize URL for OAuth Authorization Code flow.
    """
    if not state:
        state = _generate_state()
    scope_str = " ".join(scopes)
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": scope_str,
        "state": state,
        "show_dialog": "false",
    }
    from urllib.parse import urlencode
    return f"{AUTH_URL}?{urlencode(params)}", state

def exchange_code_for_tokens(code):
    """
    Exchanges authorization code for access and refresh tokens.
    """
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    resp = requests.post(TOKEN_URL, data=data, timeout=10)
    resp.raise_for_status()
    payload = resp.json()
    access_token = payload["access_token"]
    refresh_token = payload["refresh_token"]
    expires_in = payload.get("expires_in", 3600)  # seconds
    expires_at = dj_tz.now() + timedelta(seconds=expires_in)
    scope = payload.get("scope", "")
    token_type = payload.get("token_type", "Bearer")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at,
        "scope": scope,
        "token_type": token_type,
    }

def refresh_access_token(refresh_token):
    """
    Uses refresh token to obtain a new access token.
    """
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    resp = requests.post(TOKEN_URL, data=data, timeout=10)
    resp.raise_for_status()
    payload = resp.json()
    access_token = payload["access_token"]
    expires_in = payload.get("expires_in", 3600)
    expires_at = dj_tz.now() + timedelta(seconds=expires_in)
    scope = payload.get("scope", "")
    token_type = payload.get("token_type", "Bearer")
    return {
        "access_token": access_token,
        "expires_at": expires_at,
        "scope": scope,
        "token_type": token_type,
    }

def get_valid_access_token(sp_account: SpotifyAccount):
    """
    Returns a valid access token, refreshing if needed.
    """
    if sp_account.token_expires_at <= dj_tz.now() + timedelta(seconds=30):
        refreshed = refresh_access_token(sp_account.refresh_token)
        sp_account.access_token = refreshed["access_token"]
        sp_account.token_expires_at = refreshed["expires_at"]
        sp_account.scope = refreshed.get("scope", sp_account.scope)
        sp_account.save(update_fields=["access_token", "token_expires_at", "scope", "updated_at"])
