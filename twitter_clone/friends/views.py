from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import models
from .models import FriendRequest, Friendship

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    
    if to_user == request.user:
        messages.error(request, "You can't send a friend request to yourself!")
        return redirect('profile', username=to_user.username)
    
    # Check if already friends
    if Friendship.objects.filter(
        models.Q(user1=request.user, user2=to_user) |
        models.Q(user1=to_user, user2=request.user)
    ).exists():
        messages.error(request, "You are already friends!")
        return redirect('profile', username=to_user.username)
    
    # Check if request already exists
    if FriendRequest.objects.filter(
        from_user=request.user, to_user=to_user
    ).exists():
        messages.error(request, "Friend request already sent!")
        return redirect('profile', username=to_user.username)
    
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    messages.success(request, f"Friend request sent to {to_user.username}!")
    return redirect('profile', username=to_user.username)

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    
    # Create friendship
    Friendship.objects.create(user1=friend_request.from_user, user2=request.user)
    
    # Update request status
    friend_request.status = 'accepted'
    friend_request.save()
    
    messages.success(request, f"You are now friends with {friend_request.from_user.username}!")
    return redirect('friend_requests')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.status = 'rejected'
    friend_request.save()
    
    messages.success(request, "Friend request rejected!")
    return redirect('friend_requests')

@login_required
def friend_requests(request):
    received_requests = FriendRequest.objects.filter(
        to_user=request.user, status='pending'
    )
    sent_requests = FriendRequest.objects.filter(
        from_user=request.user, status='pending'
    )
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    return render(request, 'friends/friend_requests.html', context)

@login_required
def friends_list(request):
    friendships = Friendship.objects.filter(
        models.Q(user1=request.user) | models.Q(user2=request.user)
    )
    
    friends = []
    for friendship in friendships:
        if friendship.user1 == request.user:
            friends.append(friendship.user2)
        else:
            friends.append(friendship.user1)
    
    context = {'friends': friends}
    return render(request, 'friends/friends_list.html', context)