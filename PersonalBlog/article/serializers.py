# 序列化器
from rest_framework import serializers
from article.models import Article, Category, Tag
from user_info.serializers import UserDescSerializer


class TagSerializer(serializers.ModelSerializer):
    """标签序列化器"""

    def check_tag_exists(self, validated_data):
        tag = validated_data.get('tag_name')
        if Tag.objects.filter(tag_name=tag).exists():
            raise serializers.ValidationError("标签 {} 已存在".format(tag))

    #  重写create和update方法，确保不添加重复标签
    def create(self, validated_data):
        self.check_tag_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


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
# 抽象出父类，供ArticleSerializer和ArticleDetailSerializer继承使用
class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    # 文章作者的嵌套序列化字段
    author = UserDescSerializer(read_only=True)
    # 文章分类的嵌套序列化字段
    category = CategorySerializer(read_only=True)
    # category的id字段，用于创建/更新category外键
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)
    # 文章标签字段
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='tag_name'
    )

    # 重写此方法，若输入的标签不存在则创建
    # 该方法的原本作用是将请求中的原始Json数据转化为Python表达形式（期间会对字段的有效性做初步检查）。
    # 他的执行时间比默认验证器的字段检查更早，因此可以在此方法中将需要的数据创建好，
    def to_internal_value(self, data):
        tags_data = data.get('tags')
        if isinstance(tags_data, list):  # 确定标签数据是列表
            for tag in tags_data:
                if not Tag.objects.filter(tag_name=tag).exists():
                    Tag.objects.create(tag_name=tag)
        return super().to_internal_value(data)

    def validate_category_id(self, value):
        """category_id字段的验证器"""
        # 如果获取的Value值不为空，但是却找不到相应的文章类别
        if value is not None and not Category.objects.filter(id=value).exists():
            raise serializers.ValidationError("您输入了错误的文章分类id")
        return value


class ArticleSerializer(ArticleBaseSerializer):  # HyperlinkedModelSerializer自动创建外键字段的超链接，并且隐藏掉了id字段
    """文章序列化器"""
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body':{'write_only':True}}


class ArticleDetailSerializer(ArticleBaseSerializer):
    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()

    def get_body_html(self,obj):
        return obj.get_md()[0]

    def get_toc_html(self,obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'
