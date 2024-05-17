from django.db import models
from django.conf import settings


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_room'
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friend_room'
    )
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f'{self.room_id} / {self.author} / {self.friend}'
    

class Chat(models.Model):
    room_id = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='chats'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_message'
    )
    text = models.TextField(default='')
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return f'{self.pk} / {self.datetime_created}'
