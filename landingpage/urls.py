from django.contrib import admin
from django.urls import path, include

from tweets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    # path('create-tweet/', views.tweet_create_view),
    # path('tweets/', views.tweet_list_view),
    # path('tweets/<int:tweet_id>/', views.tweet_detail_view),
    # path('api/tweets/action', views.tweet_action_view),
    # path('api/tweets/<int:tweet_id>/delete', views.tweet_delete_view),
    path('api/tweets/', include('tweets.urls'))
]
