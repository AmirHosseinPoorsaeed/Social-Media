from django.db import models
from django.conf import settings


class Notification(models.Model):
    class NotificationType(models.IntegerChoices):
        LIKE = 1, 'Like'
        FOLLOW = 2, 'Follow'
        COMMENT = 3, 'Comment'
        LIKE_COMMENT = 4, 'Like Comment'
        ADD_TO_FAVORITE = 5, 'Add To Favorite'
    
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
        related_name='notify_post',
        blank=True,
        null=True
    )
    comment = models.ForeignKey(
        'blog.Comment',
        on_delete=models.CASCADE,
        related_name='notify_comment',
        blank=True,
        null=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notify_from_user'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notify_to_user',
        blank=True,
        null=True
    )
    type = models.IntegerField(choices=NotificationType.choices)
    text = models.CharField(max_length=120, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['datetime_created'])
        ]
        ordering = ['-datetime_created']

    def __str__(self):
        return f'Post: {self.post} / Comment: {self.comment} / Sender: {self.sender} / User: {self.user} / Type: {self.get_type_display()}'
