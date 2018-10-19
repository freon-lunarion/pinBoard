from django.urls import path
from django.conf.urls import *
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.QuizBankListView.as_view(), name='index'),
    path('new', views.room_create, name='create-room'),
    path('<int:pk>/', views.QuizBankDetailView.as_view(), name='room-detail'),
    # path('<int:pk>/new', views.QuestionView.as_view(), name='index'),
    path('<int:pk>/new', views.question_create, name='create-question'),
    url(r'^vote/$',views.voteAjax),
    path('<int:pk>/tryout', views.tryout_view, name='tryout'),
    url(r'^check/$',views.checkAjax),


]