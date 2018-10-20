from django.urls import path

from django.conf.urls import *
from . import views
app_name = 'shared'
urlpatterns = [
    path('<int:pk>/vote/', views.vote, name='vote'),
    path('score/', views.score, name='user_score'),
    path('user_avatar/', views.user_avatar, name='user_avatar')
]