from django.shortcuts import get_object_or_404, render
from markupsafe import re
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    RegisterSerializer, 
    UserSerializer, 
    LoginSerializer, 
    UserProfileUpdateSerializer
)
from rest_framework import permissions, authentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import User, UserProfile

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key
        })


# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key
        })

# UserProfile Update API

class UserProfileUpdateAPI(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only authenticated users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        """
        Update users profile.
        """
        pk = request.user.id
        saved_profile = get_object_or_404(UserProfile.objects.all(), pk=pk)
        serializer = UserProfileUpdateSerializer(instance=saved_profile, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            profile_saved = serializer.save()
        return Response(serializer.data)



# Get Users List API

class UserList(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = [{"Email" : user.email, "is_student" : user.is_students, "Token" : Token.objects.get(user=user).key} 
                    for user in User.objects.all()]
        return Response(users)