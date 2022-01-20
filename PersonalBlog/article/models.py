from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdown import Markdown


class Avatar(models.Model):
    """文章标题图"""
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Tag(models.Model):
    """文章标签"""
    tag_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.tag_name


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
    # 外键———文章作者
    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,  # 级联
        related_name='articles'
    )
    # 外键————文章分类
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )
    # 外键————文章标签
    tags = models.ManyToManyField(  # 多对多关系
        Tag,
        blank=True,
        related_name='articles'
    )
    # 外键————文章标题图
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='articles'
    )

    # 将Body转换为带html标签的正文
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc 是渲染后的目录
        return md_body, md.toc

    def __str__(self):
        return self.title
