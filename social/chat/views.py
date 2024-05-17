from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.safestring import mark_safe
import json

from social.chat.models import Chat, Room


User = get_user_model()


def room_list_view(request):
    user = request.user
    rooms = Room.objects.filter(
        Q(author=user) | Q(friend=user)
    ).order_by('-datetime_created')

    return render(request, 'chat/list.html', {'rooms': rooms})


def room_choice_view(request, friend_id):
    user = request.user

    try:
        friend = User.objects.get(pk=friend_id)
    except User.DoesNotExist:
        return redirect('chat:list')
        
    room = Room.objects.filter(
        Q(author=user, friend=friend) | Q(author=friend, friend=user)
    ).first()

    if not room:
        room = Room.objects.create(author=user, friend=friend)
        return redirect('chat:room', room.room_id, friend_id)
    
    return redirect('chat:room', room.room_id, friend_id)


def room_view(request, room_id, friend_id):

    try:
        Room.objects.filter(room_id=room_id)
        friend = User.objects.get(pk=friend_id)
    except Room.DoesNotExist:
        return redirect('chat:list')
    except User.DoesNotExist:
        return redirect('chat:list')
    
    chats = Chat.objects.filter(
        room_id=room_id
    ).order_by('datetime_created')

    return render(request, 'chat/room.html', {
        'chats': chats, 
        'friend': friend,
        'room_id_json': mark_safe(json.dumps(room_id))
    })
