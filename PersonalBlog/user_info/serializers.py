# 序列化器
from django.contrib.auth.models import User
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')

    # 指定解析超链接关系的字段为username
    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'password',
        ]
        extra_fields = {
            'password': {'write_only': True},
            'is_superuser': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # 将validated_data保存为字典
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')  # 密码需要单独拿出来通过set_password方法加密后再存入数据库，而不会以明文保存
            instance.set_password(password)
        return super().update(instance, validated_data)


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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'last_name',
            'first_name',
            'email',
            'last_login',
            'date_joined'
        ]
