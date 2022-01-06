from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# 博客文章 model
class Article(models.Model):
    class Meta:
        ordering = ['-created']

    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,  # 级联
        related_name='articles'
    )

    def __str__(self):
        return self.title
