import json

from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from apps.submissions.models import StudentSubmission
from apps.projects.models import Project
from .models import UserProfile
from .permissions import ObjectPermission
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    CreateUserSerializer,
    AssignmentSerializer,
)


# @permission_classes([IsAuthenticated])
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        raise PermissionDenied()


# @permission_classes([IsAuthenticated])
class UserProfileView(APIView):
    def get(self, request, pk):
        print(pk)
        profile = UserProfile.objects.get(user=pk)
        print(profile)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, pk):
        # name, bio, github_username, avatar, current_level
        profile = UserProfile(
            **request.data
        )
        profile.user = get_user_model().objects.get(pk=pk)
        profile.save()

        return Response('Success')


@permission_classes([IsAuthenticated])
class SubmissionsViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = AssignmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(
                created_by=request.user,
                modified_by=request.user
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def list(self, request, *args, **kwargs):
        queryset = StudentSubmission.objects.filter(student=request.user.id)
        serializer = AssignmentSerializer(queryset, many=True)
        return Response(serializer.data)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
