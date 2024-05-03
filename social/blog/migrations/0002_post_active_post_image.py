# Generated by Django 5.0.4 on 2024-05-02 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=1, upload_to='post/'),
            preserve_default=False,
        ),
    ]
