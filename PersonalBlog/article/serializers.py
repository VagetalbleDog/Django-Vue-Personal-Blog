# 序列化器
from rest_framework import serializers
from article.models import Article
from user_info.serializers import UserDescSerializer


class ArticleSerializer(serializers.HyperlinkedModelSerializer):  # HyperlinkedModelSerializer自动创建外键字段的超链接，并且隐藏掉了id字段
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
