from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import Article


# Create your views here.
class NewsFeedView(TemplateView):
    template_name = 'newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeedView, self).get_context_data(**kwargs)

        context['feeds'] = Article.objects.all()

        return context


class NewsFeedDetailView(TemplateView):
    model = Article
    template_name = 'detail_feed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeedDetailView, self).get_context_data(**kwargs)

        user = self.request.user

        context['feed_detail'] = Article.objects.all()

        return context
