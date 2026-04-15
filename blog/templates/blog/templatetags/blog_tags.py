import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """Возвращает общее количество опубликованных постов."""
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Выводит последние count постов."""
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """Возвращает посты с наибольшим количеством комментариев."""
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """Преобразует текст из Markdown в HTML."""
    return mark_safe(markdown.markdown(text))
