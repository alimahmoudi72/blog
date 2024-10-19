from rest_framework import serializers
from .models import Article, Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['score']


class ArticleSerializer(serializers.ModelSerializer):

    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'average_rating', 'rating_count', 'user_rating']

    def get_user_rating(self, obj):
        """
        Return the rating given by the current user, if available.
        """
        user = self.context.get('request').user
        if user.is_authenticated:
            rating = obj.ratings.filter(user=user).first()
            if rating:
                return rating.score
        return None
