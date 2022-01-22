from article.permissions import IsAdminUserOrReadOnly
from article.models import Article, Category, Tag, Avatar
from rest_framework import viewsets
from article.serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, \
    ArticleDetailSerializer, AvatarSerializer
from rest_framework import filters


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    # 导入filters.SearchFilter类实现模糊匹配,实现对文章标题、作者、分类检索
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__username', 'category__title']

    # 根据请求方式动态获取序列化器
    def get_serializer_class(self):
        if self.action == 'list':
            """文章列表"""
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """文章分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            """文章分类列表"""
            return CategorySerializer
        else:
            """文章分类详情"""
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    """文章标签视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None


class AvatarViewSet(viewsets.ModelViewSet):
    """文章标题图视图集"""
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]
