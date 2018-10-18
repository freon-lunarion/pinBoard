from django.urls import path
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.QuizBankListView.as_view(), name='index'),
    path('new', views.room_create, name='create-room'),
    path('<int:pk>/', views.QuizBankDetailView.as_view(), name='room-detail'),
    path('new_2', views.question_create, name='index'),
]