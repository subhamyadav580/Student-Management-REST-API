import email
from rest_framework import serializers

from .models import User, UserProfile
from django.contrib.auth import authenticate


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_students', "is_staff", "is_admin")



class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password2','is_students', "is_staff", "is_admin"] 
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
        fields = ["email", "fname", "mname", "lname","bio", "image", "contact_add",
                        "gender", "age", "phone"]
                        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.fname = validated_data.get('fname', instance.fname)
        instance.mname = validated_data.get('mname', instance.mname)
        instance.lname = validated_data.get('lname', instance.lname)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.contact_add = validated_data.get('contact_add', instance.contact_add)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance
    
    


