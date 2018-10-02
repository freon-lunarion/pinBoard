from django.urls import path

from django.conf.urls import *
from . import views
app_name = 'blogs'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:pk>/post/', views.PostView.as_view(), name='post'),
    path('<int:pk>/login/', views.LoginView.as_view(), name='login'),
    path('<int:pk>/register/', views.RegisterView.as_view(), name='register'),
    path('<int:post_id>/vote/', views.vote, name='vote'),
    url(r'^login/$',views.login),
    url(r'^register/$',views.register),
    url(r'^post/$',views.post),
    url(r'^comment/$',views.comment),
]