
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # existing routes...
    path("spotify/", include("vibelab.spotify.urls")),
]
