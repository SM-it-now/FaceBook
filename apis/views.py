from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.validators import ValidationError
from django.contrib.auth import authenticate, login, logout

from contents.models import Article, Page, Comment


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
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return self.response(message='이미 존재하는 아이디입니다.', status=400)

        return self.response({'user.id': user.id})


# login
class UserLoginView(BaseView):
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(message='아이디를 입력해주세요.', status=400)

        password = request.POST.get('password', '')
        if not password:
            return self.response(message='비밀번호를 입력해주세요.', status=400)

        user = authenticate(request, username=username, password=password)
        if not user:
            return self.response(message='아이디 또는 비밀번호가 일치하지 않습니다.', status=400)

        login(request, user)

        return self.response()




# article create api
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


# 뉴스피스 수정 api
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


# 뉴스피드 삭제 api
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


# 페이지 생성 api
@method_decorator(login_required, name='dispatch')
class PageCreateView(BaseView):
    def post(self, request):
        master = request.POST.get('master', '')
        if not master:
            return self.response(message='채널주인을 입력해주세요.', status=400)

        name = request.POST.get('name', '')
        if not name:
            return self.response(message='채널명을 입력해주세요.', status=400)

        text = request.POST.get('text', '')
        if not text:
            return self.response(message='내용을 입력해주세요.', status=400)

        Page.objects.create(
            master=master,
            name=name,
            text=text
        )

        return self.response({})


# page update api
class PageUpdateView(BaseView):
    def post(self, request):
        pk = request.POST.get('pk', False)
        master = request.POST.get('master', '')
        name = request.POST.get('name', '')
        text = request.POST.get('text', '')

        Page.objects.filter(pk=pk).update(
            master=master,
            name=name,
            text=text
        )

        return self.response({})


# page delete api
class PageDeleteView(BaseView):
    def post(self, request):
        try:
            page_id = request.POST.get('pk', False)
        except ValidationError:
            return self.response(message='잘못된 요청입니다.', status=400)

        try:
            page = Page.objects.filter(pk=page_id)
        except Page.DoesNotExist:
            return self.response(message='잘못된 요청입니다.', status=400)

        page.delete()

        return self.response({})


# comment create
class CommentCreateView(BaseView):
    def post(self, request):
        article_id = request.POST.get('article_id', False)
        article = Article.objects.get(pk=article_id)
        text = request.POST.get('text', '').strip()
        if not text:
            return self.response(message='댓글을 입력해주세요.', status=400)

        Comment.objects.create(
            author=self.request.user,
            article=article,
            text=text
        )

        return self.response({})


# comment delete api
class CommentDeleteView(BaseView):
    def post(self, request):
        comment_id = request.POST.get('comment_id', False)

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return self.response(message='잘못된 요청입니다.', status=400)

        comment.delete()

        return self.response({})


# like api
class LikeView(BaseView):
    def post(self, request):
        article_id = request.POST.get('like', False)
        article = Article.objects.get(pk=article_id)

        article.like.add(self.request.user)

        return self.response({})


