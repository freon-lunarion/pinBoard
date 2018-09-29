from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse

from .models import *
from shared.models import *

# Create your views here.
class IndexView(generic.ListView):
    model = QuizBank