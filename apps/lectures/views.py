from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Lecture
from .serializers import LectureSerializer

# @permission_classes([IsAuthenticated])
class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
