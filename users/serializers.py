import email
from rest_framework import serializers

from .models import User, UserProfile
from django.contrib.auth import authenticate


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_students')



class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password2','is_students']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
            user = User(
                email = self.validated_data['email'],
                is_students = self.validated_data['is_students']
            )

            password = self.validated_data['password']
            password2 = self.validated_data['password2']

            if password != password2:
                raise serializers.ValidationError({'password': 'Password must match'})

            user.set_password(password)
            user.save()

            return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        print(user)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

# User Profile Update Serializer
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["email", "name", "bio", "preferred_name", "image", 
                        "avatar_url", "discord_name", "github_username",
                        "codepen_username", "fcc_profile_url", "current_level",
                        "phone", "timezone"]



    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.preferred_name = validated_data.get('preferred_name', instance.preferred_name)
        instance.image = validated_data.get('image', instance.image)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.discord_name = validated_data.get('discord_name', instance.discord_name)
        instance.github_username = validated_data.get('github_username', instance.github_username)
        instance.codepen_username = validated_data.get('codepen_username', instance.codepen_username)
        instance.fcc_profile_url = validated_data.get('fcc_profile_url', instance.fcc_profile_url)
        instance.current_level = validated_data.get('current_level', instance.current_level)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        
        instance.save()
        return instance
    
    


