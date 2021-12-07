from django.urls import path
from .views import UserCreateView

# api url
urlpatterns = [
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user_create'),
]
