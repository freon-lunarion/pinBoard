from django.urls import path

from django.conf.urls import *
from . import views
app_name = 'blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('createArticalPost/', views.create_artical_post, name='create_artical_post'),
    path('createQuestion/', views.create_question, name='create_question'),
    path('createImagePost/', views.create_image_post, name='create_image_post'),
    path('createYoutubePost/', views.create_youtube_post, name='create_youtube_post'),
    path('<int:pk>/pin/', views.pin, name='pin'),
    path('<int:pk>/unpin/', views.unpin, name='unpin'),
    url(r'^login/$',views.login_view),
    url(r'^logout/$',views.logout_view),
    url(r'^register/$',views.register),
    url(r'^reset/$',views.reset),
]