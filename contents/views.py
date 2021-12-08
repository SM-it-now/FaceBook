from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from .models import Article


# Create your views here.
# 메인화면
class NewsFeedView(TemplateView):
    template_name = 'newsfeed.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeedView, self).get_context_data(**kwargs)

        context['feeds'] = Article.objects.all()

        return context


# 상세화면
class NewsFeedDetailView(DetailView):
    model = Article
    template_name = 'feed_detail.html'

    def get_context_data(self, **kwargs):
        context = super(NewsFeedDetailView, self).get_context_data(**kwargs)

        user = self.request.user

        context['feed'] = Article.objects.select_related('user').filter(author=user)

        return context


class FeedCreate(TemplateView):
    template_name = 'feed_create.html'
