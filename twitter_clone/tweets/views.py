from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Tweet, Reply
from .forms import TweetForm, ReplyForm
from friends.models import Friendship

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Tweet
from .forms import TweetForm
from friends.models import Friendship

@login_required
def home(request):
    # Get all friendship pairs (user1, user2)
    friendships = Friendship.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).values_list('user1', 'user2')

    # Collect all friend user IDs
    friend_ids = set()
    for u1, u2 in friendships:
        if u1 != request.user.id:
            friend_ids.add(u1)
        if u2 != request.user.id:
            friend_ids.add(u2)
    
    # Add own ID to see own tweets too
    friend_ids.add(request.user.id)

    # Get tweets from self and friends
    tweets = Tweet.objects.filter(author__id__in=friend_ids).order_by('-created_at')

    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.author = request.user
            tweet.save()
            messages.success(request, 'Your tweet was posted!')
            return redirect('home')
    else:
        form = TweetForm()

    context = {
        'tweets': tweets,
        'form': form
    }
    return render(request, 'tweets/home.html', context)


@login_required
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    replies = tweet.replies.all()
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.tweet = tweet
            reply.author = request.user
            reply.save()
            messages.success(request, 'Your reply was posted!')
            return redirect('tweet_detail', tweet_id=tweet.id)
    else:
        form = ReplyForm()
    
    context = {
        'tweet': tweet,
        'replies': replies,
        'form': form
    }
    return render(request, 'tweets/tweet_detail.html', context)

@login_required
@require_POST
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        liked = False
    else:
        tweet.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'total_likes': tweet.total_likes()
    })

@login_required
@require_POST
def retweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if tweet.retweets.filter(id=request.user.id).exists():
        tweet.retweets.remove(request.user)
        retweeted = False
    else:
        tweet.retweets.add(request.user)
        retweeted = True
    
    return JsonResponse({
        'retweeted': retweeted,
        'total_retweets': tweet.total_retweets()
    })


