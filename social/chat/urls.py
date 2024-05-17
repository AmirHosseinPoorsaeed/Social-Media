from django.urls import path

from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.room_list_view, name='list'),
    path('<int:friend_id>/', views.room_choice_view, name='choice'),
    path('room/<int:room_id>-<int:friend_id>/', views.room_view, name='room'),
]
