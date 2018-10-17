from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from shared.models import *

def index_view(request):
    rooms = QuizBank.objects.order_by('-create_time')[:12]
    pass

def room_view(request):
    
    pass

@login_required
def room_create(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")

            room = QuizBank.objects.create(
                title = request.POST['title'],
                detail = request.POST['detail'],
                submit_beginTime = request.POST['submit_beginTime'],
                submit_endTime = request.POST['submit_endTime'],
                tryout_minScore = request.POST['tryout_minScore'],
                tryout_displayNum = request.POST['tryout_displayNum'],
                tryout_beginTime = request.POST['tryout_beginTime'],
                tryout_endTime = request.POST['tryout_endTime'],
                creator = request.user,
                create_time = now,
                update_time = now

            )

            return HttpResponseRedirect(f'/quiz/{room.id}')
            
    return render(request, 'quiz/add_room.html', {'form':RegisterForm()})
    pass

class RoomView(generic.DeleteView):
    template = '*.html'
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk', "-1")
        return super(RoomView, self).dispatch(request, *args, **kwargs) 

    def get_context_data(self, **kwargs):
        room = get_object_or_404(QuizBank,id=self.pk)
        content = super(RoomView, self).get_context_data(**kwargs)
        content['questions'] = ''


def question_create(request):
    if request.method == 'POST':
        
        pass
    pass