# views.py
from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Article, Rating
from .serializers import ArticleSerializer, RatingSerializer

CACHE_TIMEOUT = 60 * 2  # Cache timeout in seconds (e.g., 2 minutes)


# Article List View
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def list(self, request, *args, **kwargs):
        """
        Overriding the default list method to implement manual caching with a custom key.
        """
        cache_key = 'article_list'  # Assign a custom cache key for the article list
        cached_data = cache.get(cache_key)  # Try to retrieve cached data

        if cached_data:
            return Response(cached_data)  # Return cached data if it exists

        # If no cached data exists, query the database and cache the response
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, CACHE_TIMEOUT)  # Cache the data with a timeout
        return response

    def get_serializer_context(self):
        """
        Pass the request context to the serializer, so it can access the current user.
        """
        return {'request': self.request}


# Submit or Update Rating View
class SubmitRatingView(generics.CreateAPIView):
    # queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        article = generics.get_object_or_404(Article, id=article_id)

        # Check if the user has already rated this article
        Rating.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'score': request.data['score']}
        )

        # After updating the rating, invalidate the article list cache
        cache.delete('article_list')

        return Response({'article_id': article_id, 'score': request.data['score']}, status=status.HTTP_200_OK)
