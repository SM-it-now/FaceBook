from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.validators import ValidationError

from contents.models import Article


# Create your views here.
# CBV Base View
@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }

        return JsonResponse(result, status=status)


# sign up
class UserCreateView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해주세요.', status=400)

        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해주세요.', status=400)

        email = request.POST.get('email', '')

        try:
            user = User.objects.create(username, email, password)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.', status=400)

        return self.response({'user.id': user.id})


# article create
@method_decorator(login_required, name='dispatch')
class FeedCreateView(BaseView):
    def post(self, request):
        author = self.request.user
        title = request.POST.get('title', '').strip()
        if not title:
            return self.response(message='제목을 입력해주세요.', status=400)

        text = request.POST.get('text', '').strip()
        if not text:
            return self.response(message='내용을 입력해주세요.', status=400)

        Article.objects.create(
            author=author,
            title=title,
            text=text
        )

        return self.response({})


@method_decorator(login_required, name='dispatch')
class FeedUpdateView(BaseView):
    def post(self, request):

        article_id = request.POST.get('pk', False)
        title = request.POST.get('title', '')
        text = request.POST.get('text', '')

        Article.objects.filter(pk=article_id).update(
            title=title,
            text=text
        )

        return self.response({})


@method_decorator(login_required, name='dispatch')
class FeedDeleteView(BaseView):
    def post(self, request):
        try:
            article_id = request.POST.get('pk', False)
        except ValidationError:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            article = Article.objects.filter(pk=article_id)
        except Article.DoesNotExist:
            return self.response(message='잘못된 요청입니다.', status=400)

        article.delete()

        return self.response({})


