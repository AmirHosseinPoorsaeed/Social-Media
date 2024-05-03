from django.urls import path, re_path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('create/', 
        views.PostCreateView.as_view(), name='post_create'
    ),
    path('user/<str:username>/',
        views.UserPostListView.as_view(), name='user_post_list'
    ),
    path('like/post/<int:post_id>/',
        views.post_like, name='post_like'
    ),
    path('like/comment/<int:comment_id>/',
        views.comment_like, name='comment_like'
    ),
    re_path(r'(?P<slug>[-\w]+)/update/',
        views.PostUpdateView.as_view(), name='post_update'
    ),
    re_path(r'(?P<slug>[-\w]+)/delete/',
        views.PostDeleteView.as_view(), name='post_delete'
    ),
    re_path(r'(?P<slug>[-\w]+)/comment/create/',
        views.CommentCreateView.as_view(), name='comment_create'
    ),
    re_path(r'(?P<slug>[-\w]+)/',
        views.PostDetailView.as_view(), name='post_detail'
    ),
]
