from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from friends.models import FriendRequest, Friendship

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile = get_object_or_404(Profile, user=user)
    tweets = user.tweet_set.all()

    is_friend = False
    friend_request_sent = False
    friend_request_received = False

    if request.user != user:
        is_friend = Friendship.objects.filter(
            models.Q(user1=request.user, user2=user) |
            models.Q(user1=user, user2=request.user)
        ).exists()

        friend_request_sent = FriendRequest.objects.filter(
            from_user=request.user, to_user=user, status='pending'
        ).exists()

        friend_request_received = FriendRequest.objects.filter(
            from_user=user, to_user=request.user, status='pending'
        ).exists()

    context = {
        'profile_user': user,
        'profile': profile,
        'tweets': tweets,
        'is_friend': is_friend,
        'friend_request_sent': friend_request_sent,
        'friend_request_received': friend_request_received,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/edit_profile.html', context)


from django.db.models import Q

@login_required
def all_users(request):
    users = User.objects.exclude(id=request.user.id)
    friends = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    )
    friend_ids = [f.user1.id if f.user2 == request.user else f.user2.id for f in friends]

    context = {
        'users': users,
        'friend_ids': friend_ids
    }
    return render(request, 'accounts/all_users.html', context)
