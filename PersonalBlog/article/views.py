from article.permissions import IsAdminUserOrReadOnly
from article.models import Article, Category
from rest_framework import viewsets
from article.serializers import ArticleSerializer, CategorySerializer,CategoryDetailSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    # 导入filters.SearchFilter类实现模糊匹配,实现对文章标题、内容、作者的检索
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'body', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """文章分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            """文章分类列表"""
            return CategorySerializer
        else:
            """文章分类详情"""
            return CategoryDetailSerializer
