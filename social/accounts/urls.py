from django.urls import path

from . import views


app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users/', views.ProfileListView.as_view(), name='user_list'),
    path('users/<str:username>/', views.ProfileDetailView.as_view(), name='user_detail'),
    path('follow/', views.follow_view, name='follow'),
]
