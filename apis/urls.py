from django.urls import path
from .views import UserCreateView
from .views import FeedCreateView, FeedUpdateView, FeedDeleteView, PageCreateView

# api url
urlpatterns = [
    path('v1/users/create/', UserCreateView.as_view(), name='apis_v1_user_create'),

    # Feed
    path('v1/feed/create/', FeedCreateView.as_view(), name='apis_v1_feed_create'),
    path('v1/feed/update/', FeedUpdateView.as_view(), name='apis_v1_feed_update'),
    path('v1/feed/delete/', FeedDeleteView.as_view(), name='apis_v1_feed_delete'),

    # Page
    path('v1/page/create/', PageCreateView.as_view(), name='apis_v1_page_create'),
]
