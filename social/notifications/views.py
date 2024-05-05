from django.shortcuts import render
from django.views import generic

from social.notifications.models import Notification


class NotificationListView(generic.ListView):
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(sender=user)
