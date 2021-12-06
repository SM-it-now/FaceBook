from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title
