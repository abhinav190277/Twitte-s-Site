from django.contrib import admin
from .models import Tweet, Reply

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'created_at', 'total_likes', 'total_retweets']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']
    readonly_fields = ['created_at']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'tweet', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content']