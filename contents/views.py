from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Article, Page


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


# 뉴스피드 생성화면
@method_decorator(login_required, name='dispatch')
class FeedCreate(TemplateView):
    template_name = 'feed_create.html'


# 뉴스피드 수정 화면
@method_decorator(login_required, name='dispatch')
class FeedUpdate(UpdateView):
    model = Article
    fields = [
        'title', 'text'
    ]
    template_name = 'feed_update.html'

    def get_context_data(self, **kwargs):
        context = super(FeedUpdate, self).get_context_data(**kwargs)

        return context


class PageView(TemplateView):
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)

        user = self.request.user

        context['pages'] = Page.objects.all()

        return context


class PageDetailView(DetailView):
    template_name = 'page_detail.html'
    model = Page

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)

        return context

