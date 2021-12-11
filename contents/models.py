from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 기본이 되는 모델
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 게시글 모델
class Article(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.pk}/'


# 페이지 모델
class Page(BaseModel):
    master = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return '{} : {}'.format(self.name, self.master)

    def get_absolute_url(self):
        return f'/{self.pk}/'
