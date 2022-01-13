from comment.models import Comment
from rest_framework import serializers
from user_info.serializers import UserDescSerializer


class CommentChildrenSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = [
            'parent_comments',
            'article'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    author = UserDescSerializer(read_only=True)

    article = serializers.HyperlinkedRelatedField(view_name='article-detail', read_only=True)
    article_id = serializers.IntegerField(write_only=True, allow_null=False, required=True)

    parent_comments = CommentChildrenSerializer(read_only=True)
    parent_comments_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    # 重写update方法，在更新时忽略parent_comments_id
    def update(self, instance, validated_data):
        validated_data.pop('parent_comments_id', None)
        return super().update(instance, validated_data)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'created': {'read_only': True}}
