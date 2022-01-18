from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password2','is_students']

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