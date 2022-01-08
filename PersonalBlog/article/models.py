from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    """文章分类"""
    title = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


# 博客文章 model
class Article(models.Model):
    class Meta:
        ordering = ['-created']  # 按文章创建时间递减

    # 标题
    title = models.CharField(max_length=100)
    # 正文
    body = models.TextField()
    # 创建时间
    created = models.DateTimeField(default=timezone.now)
    # 更新时间
    updated = models.DateTimeField(auto_now=True)
    # 外键———作者
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,  # 级联
        related_name='articles'
    )
    # 外键————分类
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )

    def __str__(self):
        return self.title

