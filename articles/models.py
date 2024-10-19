import math
from datetime import datetime, timezone

from django.db import models

from users.models import User


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)

    average_rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def update_rating(self):
        """
        Update the average rating with time-weighted scores.
        """
        # Define a time decay constant (lambda)
        time_decay_constant = 0.1

        ratings = self.ratings.all()  # Get all ratings related to the article
        total_weight_score = 0
        total_weight = 0
        current_time = datetime.now(timezone.utc)

        for rating in ratings:
            time_difference = (current_time - rating.created_at).total_seconds()
            weight = math.exp(-time_difference * time_decay_constant)

            total_weight_score += rating.score * weight
            total_weight += weight

        if total_weight > 0:
            self.average_rating = total_weight_score / total_weight
        else:
            self.average_rating = 0.0  # No ratings, set to 0

        self.rating_count = ratings.count()  # Update ratings count
        self.save()


class Rating(models.Model):
    article = models.ForeignKey(Article, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        unique_together = (('article', 'user'),)
        indexes = [models.Index(fields=['article', 'user'])]

    def __str__(self):
        return f'Rating of {self.score} for {self.article.title} by {self.user}'
