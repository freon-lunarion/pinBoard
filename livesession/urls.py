from django.urls import path

from django.conf.urls import *
from . import views
app_name = 'livesession'
urlpatterns = [
    path('', views.LiveQuestionSessionListView.as_view(), name='index'),
    path('create/', views.create_livesession, name='create_livesession'),
    path('<int:pk>/', views.LiveQuestionSessionDetailView.as_view(), name='livesession'),
]