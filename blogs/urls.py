from django.urls import path

from django.conf.urls import *
from . import views
app_name = 'blogs'
urlpatterns = [
    # path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/comments/', views.CommentView.as_view(), name='comments'),
    # path('<int:pk>/login/', views.LoginView.as_view(), name='login'),
    # path('<int:pk>/post/', views.PostView.as_view(), name='post'),
    # path('<int:pk>/register/', views.RegisterView.as_view(), name='register'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # url(r'^ajaxsubmit/$', views.ajaxsubmit),
    # url(r'^comment/$',views.comment),
    # url(r'^post/$',views.post),
    path('', views.index, name='index'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('create/', views.create_post, name='create_post'),
    path('createQuestion/', views.create_question, name='create_question'),
    url(r'^login/$',views.login_view),
    url(r'^logout/$',views.logout_view),
    url(r'^register/$',views.register),
    url(r'^vote/$',views.vote),
    url(r'^manage/$',views.manage),
]