from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        author = (
            self.request.user
            if self.request.user.is_authenticated
            else User.objects.first()
        )
        serializer.save(author=author, status=Post.Status.PUBLISHED)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
        return Comment.objects.filter(post=post, active=True)

    def perform_create(self, serializer):
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)
        serializer.save(post=post)
