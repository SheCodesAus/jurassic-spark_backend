from django.urls import path
from .views import UserRegistrationView, UserProfileView, CheckUsernameView, CustomAuthToken, MyTokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('check-username/', CheckUsernameView.as_view(), name='check-username'),
    path('token/', CustomAuthToken.as_view(), name='user-token'),
    # New JWT endpoint expected by your frontend (returns access + refresh + user_id)
    path('token/jwt/', MyTokenObtainPairView.as_view(), name='token_obtain_pair_jwt'),
]