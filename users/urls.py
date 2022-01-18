from django.urls import path
from .views import RegisterAPI, UserList

urlpatterns = [
    path('', RegisterAPI.as_view()),
    path('users', UserList.as_view())
]