from django.core.paginator import Page, Paginator
from django.db.models import Prefetch, QuerySet

from tabom.models import Article, Like


def get_an_article(user_id: int, article_id: int) -> Article:
    return Article.objects.prefetch_related(
        Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes")
    ).get(id=article_id)


def get_article_list(user_id: int, offset: int, limit: int) -> QuerySet[Article]:
    return (
        Article.objects.order_by("-id")
        .prefetch_related("like_set")
        .prefetch_related(Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes"))[
            offset : offset + limit
        ]
    )

def get_article_page(page: int, limit: int) -> Page[Article]:
    return Paginator(Article.objects.order_by("-id"), limit).page(page)