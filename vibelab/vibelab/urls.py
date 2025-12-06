"""
URL configuration for vibelab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from playlists.views import generate_share_link, get_shared_playlist, validate_access_code, spotify_login
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/playlists/', include('playlists.urls')),
    path('playlists/<uuid:playlist_id>/generate-share-link/', generate_share_link),
    path('share/<str:token>/', get_shared_playlist),
    path('share/validate/', validate_access_code),
    path('api/share/validate/', validate_access_code), #just to test password in the backend
    # path('playlists/<uuid:playlist_id>/share/', generate_share_link),
    # path('share/<uuid:id>/<str:accessCode>/', get_shared_playlist),
    path("token/spotify/", spotify_login),
]
