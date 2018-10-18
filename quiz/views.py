from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from shared.models import *


class QuizBankListView(generic.ListView):
    model = QuizBank

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class QuizBankDetailView(generic.DetailView):
    model = QuizBank
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
 
    
@login_required
def room_create(request):
    if request.method == 'POST':
        form = QuizBankForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            room = QuizBank.objects.create(
                title = request.POST['title'],
                detail = request.POST['detail'],
                tryout_minScore = request.POST['tryout_minScore'],
                tryout_displayNum = request.POST['tryout_displayNum'],
                creator = request.user
              )

            return HttpResponseRedirect(f'/quiz/{room.id}')
            
    return render(request, 'add_room.html', {'form':QuizBankForm()})
    pass



def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            quetion = Question.objects.create(
                detail = request.POST['title'],
                author = request.user,
                published_date = now
            )

            return HttpResponseRedirect(f'/quiz/{room.id}')
            
    return render(request, 'add_room.html', {'form':QuestionForm()})