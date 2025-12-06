from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Adding Simple JWT import to be able to assign a password to a playlist when shared
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True) 

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'profile_photo', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

# Adding this part to be able to assign a password to a playlist when shared
# SimpleJWT token serializer that adds user fields into the token response
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra user info to the response
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data