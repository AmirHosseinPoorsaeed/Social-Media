from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector

from social.blog.models import Post, Comment
from social.notifications.models import Notification
from social.blog.forms import CommentCreateForm, PostCreateForm
from social.blog.mixins import PostOwnerMixin


User = get_user_model()


class PostListView(generic.ListView):
    queryset = Post.objects.active()
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    paginate_by = 5


class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.get_object()
        comments = post.comments.all()
        
        post_liked = True if user in post.likes.all() else False

        context['comment_form'] = CommentCreateForm()
        context['comments'] = comments
        context['post_liked'] = post_liked

        return context


class PostCreateView(
        PostOwnerMixin,
        LoginRequiredMixin,
        generic.CreateView
    ):
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'


class PostUpdateView(
        UserPassesTestMixin,
        PostOwnerMixin,
        LoginRequiredMixin, 
        generic.UpdateView
    ):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_update.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        
        if user == obj.owner or user.is_superuser:
            return True
        return False


class PostDeleteView(
        UserPassesTestMixin,
        LoginRequiredMixin, 
        generic.DeleteView
    ):
    model = Post
    template_name = 'blog/post_delete.html'

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        
        if user == obj.owner or user.is_superuser:
            return True
        return False
    

class UserPostListView(generic.ListView):
    template_name = 'blog/user_post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Post.objects.active().filter(owner=user)


class CommentCreateView(generic.CreateView):
    form_class = CommentCreateForm

    def form_valid(self, form):
        obj = form.save(commit=False)

        user = self.request.user
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug)
        comment_id = self.request.POST.get('comment_id')

        obj.author = user
        obj.post = post

        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id)
            obj.reply = comment

        obj.save()
        
        notify = Notification(
            sender=user,
            post=post,
            comment=obj, 
            text=obj.body, 
            type=3
        )
        notify.save()
        
        return super().form_valid(form)
    

class SearchListView(generic.ListView):
    template_name = 'blog/post_search_list.html'
    context_object_name = 'posts'

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('q')
        return Post.objects.active()\
            .annotate(search=SearchVector('title', 'owner__username'))\
            .filter(search=query)
    

class WishListView(generic.ListView):
    template_name = 'blog/post_wish_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        return Post.objects.active().filter(favorites=user)
    

class UserPostLikeView(generic.ListView):
    template_name = 'blog/post_user_like_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = self.request.user
        return user.post_likes.active()
    

def post_favorite(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.favorites.all():
        post.favorites.remove(user)
        notify = Notification.objects.filter(post=post, sender=user, type=5)
        notify.delete()        
    else:
        post.favorites.add(user)
        notify = Notification(post=post, sender=user, type=5)
        notify.save()

    return redirect(post.get_absolute_url())


def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        notify = Notification.objects.filter(post=post, sender=user, type=1)
        notify.delete()
    else:
        post.likes.add(user)
        notify = Notification(post=post, sender=user, type=1)
        notify.save()

    return redirect(post.get_absolute_url())


def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        notify = Notification.objects.filter(comment=comment, sender=user, type=4)
        notify.delete()
    else:
        comment.likes.add(user)
        notify = Notification(comment=comment, sender=user, type=1)
        notify.save()

    return redirect(comment.get_absolute_url())
