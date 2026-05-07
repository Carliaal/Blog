from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from posts.models import Post
from .forms import EditProfileForm
from .models import Profile

User = get_user_model()

def users_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'users/profile/list.html', {'users': users})


def profile_detail(request, username):
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    profile, _ = Profile.objects.get_or_create(user=profile_user)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at', '-id')
    return render(request, 'users/profile/detail.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'is_own': request.user == profile_user,
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile-detail', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'users/profile/edit.html', {'form': form})
