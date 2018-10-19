from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib import auth
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils import timezone
import datetime
from django.shortcuts import redirect
import json

# Create your views here.

def vote(request, pk):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        vote =  data['vote']
        if (int(vote) == 0):
            return JsonResponse({'exist': Vote.exist(pk, request.user.id)})
        return JsonResponse({'score': Vote.vote(pk, request.user.id, vote)})