# views.py
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer

CACHE_TIMEOUT = 60 * 2  # Cache timeout in seconds (e.g., 2 minutes)


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        """
        Implement get method and manual caching with a custom key.
        """
        cache_key = 'article_list'  # Assign a custom cache key for the article list
        cached_data = cache.get(cache_key)  # Try to retrieve cached data

        if cached_data:
            return Response(cached_data)

        # If no cached data exists, query the database and cache the response
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TIMEOUT)  # Cache the data with a timeout
        return response

    def get_serializer_context(self):
        """
        Pass the request context to the serializer, so it can access the current user.
        """
        return {'request': self.request}


class SubmitRatingView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Submit or update rating and invalidate cache.
        """

        article_id = kwargs.get('article_id')
        article = generics.get_object_or_404(Article, id=article_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score = serializer.validated_data['score']

        # Check if the user has already rated this article
        Rating.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'score': score}
        )

        # After updating the rating, invalidate the article list cache
        cache.delete('article_list')

        return Response(serializer.data)
