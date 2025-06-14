from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),
    path('retweet/<int:tweet_id>/', views.retweet, name='retweet'),
]