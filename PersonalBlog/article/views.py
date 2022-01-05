from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, mixins, generics
from django.http import Http404
from article.permissions import IsAdminUserOrReadOnly
from article.models import Article
from article.serializers import ArticleDetailSerializer, ArticleListSerializer


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAdminUserOrReadOnly]  # 用于权限控制
