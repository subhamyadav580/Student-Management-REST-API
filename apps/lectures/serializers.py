from .models import Lecture
from rest_framework import serializers

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'title', 'description',
                  'lecturer_name', 'date', 'duration',
                  'slides_url', 'level', 'required')