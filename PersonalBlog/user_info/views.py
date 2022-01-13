from django.shortcuts import render
from user_info.permissions import IsSelfOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from user_info.serializers import UserRegisterSerializer, UserDetailSerializer


# Create your views here.
class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method == 'POST':  # 注册用户的请求POST是所有人都允许操作的
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    # 自定义动作
    @action(detail=True, methods=['get'])  # 在详情页面中，提供extra——actions info 可以查询更加详细的信息
    def info(self, request, username=None):
        queryset = User.objects.get(username=username)
        serializer = UserDetailSerializer(queryset, many=False)
        return Response(serializer.data)

    @action(detail=False)
    def sorted(self, request):
        users = User.objects.all().order_by('date_joined')

        page = self.paginate_queryset(users)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def super_user(self, request):
        users = User.objects.filter(is_superuser=1)

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def normal_user(self, request):
        users = User.objects.filter(is_superuser=0)

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)