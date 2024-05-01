from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from PIL import Image


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    following = models.ManyToManyField(
        'self',
        related_name='followers',
        symmetrical=False,
        blank=True
    )
    bio = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='profile/', default='default-avatar.jpg')
    birth_date = models.DateField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output_size_image = (300, 300)
            image.thumbnail(output_size_image)
            image.save(self.image.path)

    @property
    def count_following(self):
        return self.following.count()
    
    @property
    def count_followers(self):
        return self.followers.count()
