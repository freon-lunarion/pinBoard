
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
from django.views.decorators.csrf import csrf_protect
from shared.models import *

class QuizBankListView(generic.ListView):
    model = QuizBank

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

class QuizBankDetailView(generic.DetailView):
    model = QuizBank
    
    @method_decorator(login_required,csrf_protect)
    def dispatch(self, *args, **kwargs):
        self.pk = kwargs.get('pk', "-1")
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(QuizBankDetailView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(quizBank=self.pk)[:60]
        
        return context
 
    
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

def question_create(request,pk):
    quizBank = QuizBank.objects.get(pk= pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            question = Question.objects.create(
                quizBank = quizBank,
                detail = request.POST['detail'],
                author = request.user,
                published_date = now
            )

            for i in range(4):
                option = request.POST["options_{}".format(i)]
                isCorrect = False
                try:
                    if request.POST["true_{}".format(i)] == 'on':
                        isCorrect = True
                except:
                    pass
                Options.objects.create(question = question, detail = option, isCorrect = isCorrect)

            return HttpResponseRedirect(f'/quiz/{quizBank.id}')
    
    form = QuestionForm(initial={'quizBank': quizBank})
    return render(request, 'add_room.html', {'form':form})

@login_required
def voteAjax(request):
    if (request.method == 'GET'):
        data = request.GET
        val = data.get('voteVal')
        qId = data.get('qId')
        question = get_object_or_404(Question,id = qId)
        
        if  Vote.objects.filter(content=question, user=request.user).exists() :
            
            return HttpResponse(status=208)

        else:
            repsonse = Vote.objects.create(
                content = question,
                user = request.user,
                value = val
            )
            return HttpResponse(status=201)
