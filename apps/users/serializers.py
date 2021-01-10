from apps.users.models import *
from apps.projects.models import *
from apps.submissions.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'is_student')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        is_student = validated_data.pop('is_student')
        user = get_user_model().objects.create_user(**validated_data)
        user.is_student = is_student
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
                queryset=get_user_model().objects.all())

    class Meta:
        model = UserProfile
        fields = ('__all__')


class CreateUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
                queryset=get_user_model().objects.all())

    class Meta:
        model = UserProfile
        fields = ('__all__')


class AssignmentSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
                queryset=Project.objects.all())
    student = serializers.PrimaryKeyRelatedField(
                queryset=get_user_model().objects.all())
    url = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return StudentSubmission.objects.create(**validated_data)

    class Meta:
        model = StudentSubmission
        fields = ('id', 'project', 'student',
                  'url', 'feedback', 'approved')
        read_only_fields = ['feedback', 'approved']