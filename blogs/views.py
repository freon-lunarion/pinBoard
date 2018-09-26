from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Post, Comment

# Create your views here.
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

def vote(request, post_id):
    ... # same as above, no changes needed.