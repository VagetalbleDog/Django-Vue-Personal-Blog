# 序列化器
from django.contrib.auth.models import User
from rest_framework import serializers


class UserDescSerializer(serializers.ModelSerializer):
    """在文章列表中引用的嵌套序列化容器"""

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_login',
            'date_joined'
        ]