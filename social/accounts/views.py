from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from social.accounts.forms import \
    UserUpdateForm, \
    ProfileUpdateForm
from social.accounts.models import Profile


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        return render(request, 'accounts/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request):
        user_form = UserUpdateForm(
            request.POST, instance=request.user
        )
        profile_form = ProfileUpdateForm(
            request.POST, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')


class ProfileListView(generic.ListView):
    template_name = 'accounts/profile_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs.get('username')
        profile = get_object_or_404(Profile, user__username=username)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        profile = self.get_object()

        if user.profile in profile.followers.all():
            follow = True
        else:
            follow = False

        context['follow'] = follow
        return context


def follow_view(request):
    if request.method == 'POST':
        my_profile = get_object_or_404(Profile, user=request.user)
        obj_pk = request.POST.get('profile_pk')
        obj = get_object_or_404(Profile, pk=obj_pk)

        if obj in my_profile.following.all():
            my_profile.following.remove(obj.user.profile)
        else:
            my_profile.following.add(obj.user.profile)

        return redirect(request.META.get('HTTP_REFERER'))

    return redirect('accounts:users_list')
