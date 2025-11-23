
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from vibelab.spotify.services.auth_service import get_authorize_url, exchange_code_for_tokens
from vibelab.spotify.models import SpotifyAccount

# You can store state in session to validate on callback
@require_GET
@login_required
def spotify_login(request):
    authorize_url, state = get_authorize_url()
    request.session["spotify_oauth_state"] = state
    return HttpResponseRedirect(authorize_url)

@require_GET
@login_required
def spotify_callback(request):
    state_expected = request.session.get("spotify_oauth_state")
    state_received = request.GET.get("state")
    code = request.GET.get("code")
    error = request.GET.get("error")

    if error:
        return HttpResponseBadRequest(f"Spotify auth error: {error}")

    if not code or not state_received or state_received != state_expected:
        return HttpResponseBadRequest("Invalid state or missing code")

    tokens = exchange_code_for_tokens(code)

    # Fetch the user's Spotify profile to get spotify_user_id
    # Using the access token we just got
    import requests
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    me_resp = requests.get("https://api.spotify.com/v1/me", headers=headers, timeout=10)
    me_resp.raise_for_status()
    me = me_resp.json()
    spotify_user_id = me["id"]

    sp_account, _ = SpotifyAccount.objects.update_or_create(
        spotify_user_id=spotify_user_id,
        defaults={
            "user": request.user,
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_expires_at": tokens["expires_at"],
            "scope": tokens.get("scope", ""),
        },
    )

    # Clean up state
    request.session.pop("spotify_oauth_state", None)

    # Redirect or respond; for dev, simple JSON:
    return JsonResponse({
        "status": "connected",
        "spotify_user_id": spotify_user_id,
        "scopes": tokens.get("scope", ""),
        "token_expires_at": tokens["expires_at"].isoformat(),
    })
