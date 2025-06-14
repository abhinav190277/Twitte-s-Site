from django.urls import path
from . import views

urlpatterns = [
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('requests/', views.friend_requests, name='friend_requests'),
    path('list/', views.friends_list, name='friends_list'),
]