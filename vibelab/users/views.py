from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, MyTokenObtainPairSerializer
from django.contrib.auth import get_user_model

# Adding Simple JWT import to be able to assign a password to a playlist when shared
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class CheckUsernameView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get("username", "")

        if not username:
            return Response({"error": "Username is required"}, status=400)

        exists = User.objects.filter(username=username).exists()

        return Response({"exists": exists})


class CustomAuthToken(ObtainAuthToken):
    """
    Existing TokenAuth endpoint (keeps returning token + user_id).
    You can keep this if other clients rely on it.
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response({"token": token.key, "user_id": token.user_id})


# Adding this part to be able to assign a password to a playlist when shared
class MyTokenObtainPairView(TokenObtainPairView):
    """
    New JWT endpoint that uses the MyTokenObtainPairSerializer to include user_id.
    POST to this endpoint with {"username": "...", "password": "..."} to get
    {"refresh": "...", "access": "...", "user_id": ..., "username": "..."}
    """

    serializer_class = MyTokenObtainPairSerializer
