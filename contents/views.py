from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Article


# Create your views here.
class NewsFeedView(TemplateView):
    template_name = 'newsfeed.html'

