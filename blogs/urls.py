from django.urls import path

from . import views
app_name = 'blogs'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/post/', views.PostView.as_view(), name='post'),
    path('<int:post_id>/vote/', views.vote, name='vote'),
]