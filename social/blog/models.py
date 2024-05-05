from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from ckeditor.fields import RichTextField

from social.blog.managers import PostManager


class Post(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='post_likes',
        blank=True
    )
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostFavorite',
        related_name='post_favorites',
        blank=True
    )
    image = models.ImageField(upload_to='post/')
    active = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    @property
    def count_likes(self):
        return self.likes.count()
    

class PostFavorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE
    )
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Post Favorite'
        verbose_name_plural = 'Posts Favorites'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    body = models.TextField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='comment_likes',
        blank=True
    )
    reply = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        blank=True,
        null=True
    )
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f'{self.author} - {self.post.title}'
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.post.slug])

    @property
    def count_likes(self):
        return self.likes.count()
    