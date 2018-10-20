from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.contrib import auth
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.utils import timezone
import datetime
from django.shortcuts import redirect
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

def vote(request, pk):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        vote =  data['vote']
        if (int(vote) == 0):
            return JsonResponse({'exist': Vote.exist(pk, request.user.id)})
        return JsonResponse({'score': Vote.vote(pk, request.user.id, vote)})

def score(request):
    if (request.method == 'GET'):
        return JsonResponse({'score': sum([c.score for c in Content.objects.filter(author=request.user)])})

def user_avatar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.user.userprofile.avatar = data['avatar']
        request.user.userprofile.save()
        request.session['avatar'] = data['avatar']
        return JsonResponse({'message': 'Succeed'})