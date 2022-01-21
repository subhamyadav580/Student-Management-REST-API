from django.urls import path
from .views import (
    RegisterAPI, 
    UserList, 
    LoginAPI,
    UserProfileUpdateAPI
)

urlpatterns = [
    path('', RegisterAPI.as_view()),
    path('users', UserList.as_view()),
    path('login', LoginAPI.as_view()),
    path('updateprofile', UserProfileUpdateAPI.as_view())
]