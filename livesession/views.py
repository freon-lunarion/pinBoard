from django.shortcuts import render
from django.views import generic
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.
class LiveQuestionSessionListView(generic.ListView):
    model = LiveQuestionSession
    template_name = 'index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class LiveQuestionSessionDetailView(generic.DetailView):
    model = LiveQuestionSession

    @method_decorator(login_required, csrf_protect)
    def dispatch(self, *args, **kwargs):
        self.pk = kwargs.get('pk', "-1")
        return super().dispatch(*args, **kwargs)

def create_livesession(request):
    if (request.method == 'POST'):
        form = AddLiveQuestionSessionForm(request.POST)
        if form.is_valid():
            #publish = form.cleaned_data['publish']
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            tags = form.cleaned_data['tags'].split(',')
            #if (publish):
            post = LiveQuestionSession.objects.create(title=form.cleaned_data['title'],
                                detail=form.cleaned_data['detail'],
                                author= request.user,
                                published_date=now
                               )
            for title in tags:
                if title.strip() == '':
                    continue
                exist_tag = Tag.objects.filter(title=title.strip())
                if exist_tag.count() != 0:
                    ContentTag.create(post.id, exist_tag.first().id)
                else:
                    ContentTag.create(post.id, Tag.create(title.strip()).id)
            return HttpResponseRedirect(f'/livesession/{post.id}')
        return render(request, 'add_live_session.html', {'form': AddLiveQuestionSessionForm()})
    return render(request, 'add_live_session.html', {'form': AddLiveQuestionSessionForm()})