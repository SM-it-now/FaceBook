from django.urls import path
from .views import UserCreateView
from .views import FeedCreateView, FeedUpdateView

# api url
urlpatterns = [
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user_create'),

    # Feed
    path('v1/feed/create/', FeedCreateView.as_view(), name='apis_v1_feed_create'),
    path('v1/feed/update/', FeedUpdateView.as_view(), name='apis_v1_feed_update'),
]
