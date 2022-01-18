from django.urls import path
from .views import RegisterAPI

urlpatterns = [
    path('', RegisterAPI.as_view())
]