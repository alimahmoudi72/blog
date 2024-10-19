# Generated by Django 5.1.2 on 2024-10-19 18:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='rating',
            index=models.Index(fields=['article', 'user'], name='articles_ra_article_95175e_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('article', 'user')},
        ),
    ]
