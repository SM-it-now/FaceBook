from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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
        title = request.POST.get('title', '').strip()
        if not title:
            return self.response(message='제목을 입력해주세요.', status=400)

        text = request.POST.get('text', '').strip()
        if not text:
            return self.response(message='제목을 입력해주세요.', status=400)

        article = Article.objects.filter(title=self.title, text=self.text).update(
            title=title,
            text=text
        )
        article.save()

        return self.response({})





