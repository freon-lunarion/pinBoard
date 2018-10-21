from django.urls import path
from django.conf.urls import *
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.QuizBankListView.as_view(), name='index'),
    path('<int:pk>/', views.QuizBankDetailView.as_view(), name='room-detail'),
    path('<int:pk>/create', views.question_create, name='create-question'),
    path('<int:pk>/tryout', views.tryout_view, name='tryout'),
    path('create', views.room_create, name='create-room'),
    path('<int:pk>/edit/',views.room_update, name="room-update"),
    url(r'^check/$',views.checkAjax),
    url(r'^vote/$',views.voteAjax),
]