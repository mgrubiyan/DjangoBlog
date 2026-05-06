from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.PostListAPIView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<slug:post_slug>/comments/', views.CommentListCreateView.as_view(),
         name='comment_list_create'),
]
