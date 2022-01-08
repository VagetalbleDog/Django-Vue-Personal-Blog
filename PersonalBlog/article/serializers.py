# 序列化器
from rest_framework import serializers
from article.models import Article, Category
from user_info.serializers import UserDescSerializer


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created']


class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情中嵌套的包含的文章的序列化器"""
    Article_url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Article
        fields = [
            'Article_url',
            'title'
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'created',
            'articles'
        ]


class ArticleSerializer(serializers.HyperlinkedModelSerializer):  # HyperlinkedModelSerializer自动创建外键字段的超链接，并且隐藏掉了id字段
    """文章序列化器"""
    # 文章作者的嵌套序列化字段
    author = UserDescSerializer(read_only=True)
    # 文章分类的嵌套序列化字段
    category = CategorySerializer(read_only=True)
    # category的id字段，用于创建/更新category外键
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    def validate_category_id(self, value):
        """category_id字段的验证器"""
        # 如果获取的Value值不为空，但是却找不到相应的文章类别
        if value is not None and not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("您输入了错误的文章分类id")
        return value

    class Meta:
        model = Article
        fields = '__all__'
