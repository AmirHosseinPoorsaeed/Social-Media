from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model

from social.blog.models import Post, Comment
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

        obj.author = user
        obj.post = post
        
        return super().form_valid(form)


def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(post.get_absolute_url())


def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return redirect(comment.get_absolute_url())
