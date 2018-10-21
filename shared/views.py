from .forms import *
from .models import *
from blogs.models import Post,QnaQuestion
from quiz.models import QuizBank
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404,redirect, render,render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.utils import timezone
from django.views import generic
import datetime
import json
# Create your views here.

@login_required
def vote(request, pk):
    if (request.method == 'POST'):
        data = json.loads(request.body)
        vote =  data['vote']
        if (int(vote) == 0):
            return JsonResponse({'exist': Vote.exist(pk, request.user.id)})
        return JsonResponse({'score': Vote.vote(pk, request.user.id, vote)})

@login_required
def score(request):
    if (request.method == 'GET'):
        return JsonResponse({'score': sum([c.score for c in Content.objects.filter(author=request.user)])})

@login_required
def user_avatar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        request.user.userprofile.avatar = data['avatar']
        request.user.userprofile.save()
        request.session['avatar'] = data['avatar']
        return JsonResponse({'message': 'Succeed'})

@login_required
def user_profile(request, pk):

    profile = UserProfile.objects.get(pk=pk)
    article = Post.objects.filter(author=profile.user,kind='Post')
    images = Post.objects.filter(author=profile.user,kind='Image')
    qna = QnaQuestion.objects.filter(author=profile.user,kind='Question')
    quiz = QuizBank.objects.filter(creator=profile.user)

    context = {
        'profile' : profile,
        'article' : article,
        'images' : images,
        'qna' : qna,
        'quiz' : quiz
    }
    
    return render(request,'shared/user_profile.html',context=context)

@login_required
def user_like(request, pk):
    if request.method == 'POST':
        UserFavorite.create(pk, request.user.id)
        return JsonResponse({'message': 'Succeed'})

@login_required
def user_unlike(request, pk):
    if request.method == 'POST':
        UserFavorite.objects.get(content__id=pk, user=request.user).delete()
        return JsonResponse({'message': 'Succeed'})