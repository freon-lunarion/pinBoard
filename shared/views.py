from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from .models import *
from django.contrib import auth
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils import timezone
import datetime
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def vote(request, pk):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        user = data['user']
        vote =  data['vote']
        if (vote == 0):
            return HttpResponse(str(Vote.exist(pk, user)))
        return HttpResponse(str(Vote.vote(pk, user, vote)))