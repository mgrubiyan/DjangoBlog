from rest_framework import serializers
from blog.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'body', 'publish', 'status', 'author', 'tags']
        read_only_fields = ['id', 'publish', 'author', 'tags']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'email', 'body', 'created', 'active']
        read_only_fields = ['created', 'active']
