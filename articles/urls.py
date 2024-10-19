from django.urls import path
from .views import ArticleListView, SubmitRatingView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('article/<int:article_id>/rate/', SubmitRatingView.as_view(), name='submit-rating'),
]