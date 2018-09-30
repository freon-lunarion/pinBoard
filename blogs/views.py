from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse

from .models import Post, Comment
from shared.models import *
from django.contrib import auth
from django.shortcuts import render,render_to_response


# Create your views here.
def index(request):
    latest_post_list = Post.objects.order_by('-create_time')[:5]
    # latest_post_list = Post.objects.all()
    context = {
        'latest_post_list': latest_post_list,
    }

    return render(request, 'blogs/index.html', context=context)


class IndexView(generic.ListView):
    template_name = 'blogs/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Post.objects.order_by('-create_time')[:5]


class DetailView(generic.DetailView):
    model = Post
    template_name = 'blogs/detail.html'


class ResultsView(generic.DetailView):
    model = Post
    template_name = 'blogs/results.html'

class PostView(generic.DetailView):
    model = Post
    template_name = 'blogs/post.html'

class LoginView(generic.DetailView):
    model = Post
    template_name = 'blogs/login.html'



def vote(request, content_id):
    if (request.method == 'POST'):
        user_id = request.POST.get('user_id', None)
        value = request.POST.get('value', 1)
        return HttpResponse(str(Vote.vote(content_id, user_id, value)))



def login(request):
    if (request.method == 'POST'):
        name = request.POST.get['username']
        password = request.POST.get['password']
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(req,user)
            return render_to_response('index.html', RequestContext(req))
        else:
            return render_to_response('login.html', RequestContext(req, {'password_is_wrong': True}))



