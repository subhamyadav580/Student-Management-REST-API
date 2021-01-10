from rest_framework import serializers

class GithubCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255, required=True)
    clientId = serializers.CharField(max_length=255)
    redirectUri = serializers.CharField(max_length=255)
