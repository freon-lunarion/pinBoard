from django.urls import path

from django.conf.urls import *
from . import views
app_name = 'shared'
urlpatterns = [
    path('vote/', views.vote, name='vote'),
]