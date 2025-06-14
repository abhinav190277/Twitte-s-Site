from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)
    retweets = models.ManyToManyField(User, related_name='retweeted_tweets', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"

    def total_likes(self):
        return self.likes.count()

    def total_retweets(self):
        return self.retweets.count()

class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply by {self.author.username} to {self.tweet.author.username}"