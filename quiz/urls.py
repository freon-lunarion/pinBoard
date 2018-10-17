from django.urls import path

from . import views
app_name = 'quiz'
urlpatterns = [
    path('', views.index_view, name='index'),
    path('new', views.room_create, name='index'),
    path('<int:pk>/', views.room_create, name='index'),
]