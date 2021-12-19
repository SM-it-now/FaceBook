"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.shortcuts import redirect

from contents.views import NewsFeedView, NewsFeedDetailView, FeedCreate, FeedUpdate
from contents.views import PageView, PageDetailView, PageCreate, PageUpdate



class NonUserTemplateView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('newsfeed')
        return super(NonUserTemplateView, self).dispatch(request, *args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/', include('apis.urls')),

    # user
    path('register/', NonUserTemplateView.as_view(template_name='user/register.html'), name='register'),
    path('login/', NonUserTemplateView.as_view(template_name='user/login.html'), name='login'),

    # feed
    path('', NewsFeedView.as_view(), name='newsfeed'),
    path('<int:pk>/', NewsFeedDetailView.as_view(), name='feed_detail'),
    path('feed/create/', FeedCreate.as_view(), name='feed_create'),
    path('<int:pk>/update/', FeedUpdate.as_view(), name='feed_update'),
    # feed delete --> api로 추가함.

    # page
    path('pages/', PageView.as_view(), name='page'),
    path('pages/<int:pk>/', PageDetailView.as_view(), name='page_detail'),
    path('pages/create/', PageCreate.as_view(), name='page_create'),
    path('pages/<int:pk>/update/', PageUpdate.as_view(), name='page_update'),
]
