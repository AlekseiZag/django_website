from django.contrib import admin
from django.urls import path

from tweets import views

urlpatterns = [

    path('', views.tweet_list_view),
    path('action/', views.tweet_action_view),
    path('create/', views.tweet_create_view),
    path('<int:tweet_id>/', views.tweet_detail_view),
    path('<int:tweet_id>/delete/', views.tweet_delete_view),
]
