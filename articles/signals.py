from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Rating


# Signal handler to update the article's rating when a rating is saved
@receiver(post_save, sender=Rating)
def update_article_rating_on_save(sender, instance, **kwargs):
    instance.article.update_rating()
