from django.contrib import admin

from articles.models import Article, Rating


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ('average_rating', 'rating_count')
    list_display = ['title', 'body']
    list_filter = ['title', ]
    search_fields = ['title', ]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'score']
