# Generated by Django 5.0.4 on 2024-05-14 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='friend',
        ),
    ]
