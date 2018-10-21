from django.urls import path

from django.conf.urls import *
from . import views
app_name = 'shared'
urlpatterns = [
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('score/', views.score, name='user_score'),
    path('user_avatar/', views.user_avatar, name='user_avatar'),
    path('user/<int:pk>', views.user_profile, name='user_profile'),
    path('<int:pk>/user_like/', views.user_like, name='user_like'),
    path('<int:pk>/user_unlike/', views.user_unlike, name='user_unlike')
]