from django.contrib import admin

from social.chat.models import Chat, Room


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'author', 'datetime_created',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'author', 'friend', 'datetime_created',)