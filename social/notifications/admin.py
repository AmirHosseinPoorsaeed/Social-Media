from django.contrib import admin

from social.notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'comment', 'sender', 'user', 'type',)
