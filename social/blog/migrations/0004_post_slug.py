# Generated by Django 5.0.4 on 2024-05-02 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_comment_likes_alter_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
