from .forms import *
from .models import Post, Comment, QnaQuestion, QnaAnswer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from shared.models import *
import datetime
import simplejson as json
from django.template.loader import render_to_string


# Create your views here.
# class IndexView(generic.ListView):
#     template_name = 'blogs/index.html'
#     context_object_name = 'latest_post_list'

#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Post.objects.order_by('-create_time')[:5]

# class DetailView(generic.DetailView):
#     model = Post
#     template_name = 'blogs/detail.html'


# class ResultsView(generic.DetailView):
#     model = Post
#     template_name = 'blogs/results.html'

class PostView(generic.DetailView):
    model = Content
    template_name = 'blogs/post.html'

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk', "-1")
        return super(PostView, self).dispatch(request, *args, **kwargs)

    # content: post, comments (list), comment_form
    def get_context_data(self, **kwargs):
        content = get_object_or_404(Content, id=self.pk)
        context = super(PostView, self).get_context_data(**kwargs)
        post_res = Post.objects.all().filter(id=content.id)
        if post_res.count() == 1:
            post = post_res[0]
            context['post'] = post
            context['comments'] = sorted(Comment.objects.filter(parent=post),
                                         key=lambda x: (x.score, -x.published_date.toordinal() if x.published_date
                                         else 0), reverse=True)
            context['comment_form'] = CommentForm()
        else:
            question = get_object_or_404(QnaQuestion, id=self.pk)
            context['post'] = question

        return context

    # redirecting. let me know if it should not be redirecting - Deanna
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, id=self.pk)
            # user = form.cleaned_data['comment_user']
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            Comment.objects.create(parent=post,
                                detail=form.cleaned_data['comment_detail'],
                                author= request.user,
                                published_date=now)
            return HttpResponseRedirect(f'/blogs/{self.pk}')
        return HttpResponseRedirect(f'/blogs/{self.pk}')

class QuestionView(generic.DetailView):
    model = QnaQuestion
    template_name = 'blogs/post.html'

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk', "-1")
        return super(QuestionView, self).dispatch(request, *args, **kwargs)

    # content: post, comments (list), comment_form
    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, id=self.pk)
        context = super(QuestionView, self).get_context_data(**kwargs)
        context['comments'] = sorted(Comment.objects.filter(parent=post),
                                     key=lambda x: (x.score, -x.published_date.toordinal() if x.published_date
                                     else 0), reverse=True)
        context['vote'] = sorted(Vote.objects.filter(content=post))
        context['comment_form'] = CommentForm()
        return context

    # redirecting. let me know if it should not be redirecting - Deanna
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = get_object_or_404(Post, id=self.pk)
            # user = form.cleaned_data['comment_user']
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            Comment.objects.create(parent=post,
                                   detail=form.cleaned_data['comment_detail'],
                                   author=request.user,
                                   published_date=now)
            return HttpResponseRedirect(f'/blogs/{self.pk}')
        return HttpResponseRedirect(f'/blogs/{self.pk}')


# class CommentView(generic.ListView):
#     template_name = 'blogs/comment.html'
#     context_object_name = 'comment_list'

#     # dispatch is called when the class instance loads
#     def dispatch(self, request, *args, **kwargs):
#         self.pk = kwargs.get('pk', "-1")
#         return super(generic.ListView, self).dispatch(request, *args, **kwargs)

#     def get_queryset(self):
#         """Return the comments of the certain post ordered by score."""
#         return sorted(Comment.objects.filter(parent=self.pk), key=lambda c: (c.score, c.published_date.toordinal()
#                                       if c.published_date else 0), reverse=True)

# class LoginView(generic.DetailView):
#     model = Post
#     template_name = 'blogs/login.html'

# class RegisterView(generic.DetailView):
#     model = Post
#     template_name = 'blogs/register.html'
@login_required
def index(request):
    latest_post_list = sorted(Post.objects.all(), key=lambda p: (p.score, p.published_date.toordinal()
                                                                 if p.published_date else 0), reverse=True)
    latest_question_list = sorted(QnaQuestion.objects.all(), key=lambda q: (q.score, q.published_date.toordinal()
                                                                 if q.published_date else 0), reverse=True)

    # get comment counts
    for post in latest_post_list:
        count = Comment.objects.filter(parent=post).count()
        if count == 0:
            count_string = "No Comments"
        if count == 1:
            count_string = "1 Comment"
        if count > 1:
            count_string = str(count) + ' Comments'
            # count_string = count.append(' Comments')
            
        post.comments = count_string

    for question in latest_question_list:
        count = QnaAnswer.objects.filter(parent=question).count()
        if count == 0:
            count_string = "No Answers"
        if count == 1:
            count_string = "1 Answer"
        if count > 1:
            count_string = str(count) + ' Answers'

        question.answers = count_string

    # latest_post_list = Post.objects.all()
    context = {
        'latest_post_list': latest_post_list + latest_question_list,
    }

    return render(request, 'blogs/index.html', context=context)

@login_required
def create_post(request):
    if (request.method == 'POST'):
        form = AddPostForm(request.POST)
        if form.is_valid():
            #publish = form.cleaned_data['publish']
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            tags = form.cleaned_data['tags'].split(',')
            #if (publish):
            post = Post.objects.create(title=form.cleaned_data['title'],
                                is_pinned=False,
                                pin_board=None,
                                operator=None,
                                detail=form.cleaned_data['detail'],
                                author= request.user,
                                published_date=now
                               )
            for title in tags:
                tag = Tag.create(title.strip())
                ContentTag.create(post.id, tag.id)
            return HttpResponseRedirect(f'/blogs/{post.id}')
        return render(request, 'blogs/add_post.html', {'form': AddPostForm()})
    return render(request, 'blogs/add_post.html', {'form': AddPostForm()})

@login_required
def create_image_post(request):
    if (request.method == 'POST'):
        form = AddPostForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            post = Post.objects.create(title=form.cleaned_data['title'],
                                is_pinned=False,
                                pin_board=None,
                                operator=None,
                                kind='Image',
                                detail=form.cleaned_data['detail'],
                                author= request.user,
                                published_date=now
                               )
            return HttpResponseRedirect(f'/blogs/{post.id}')

@login_required
def create_question(request):
    if (request.method == 'POST'):
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            # publish = form.cleaned_data['publish']
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            tags = form.cleaned_data['tags'].split(',')
            # if (publish):
            question = QnaQuestion.objects.create(title=form.cleaned_data['title'],
                                       detail=form.cleaned_data['detail'],
                                       author=request.user,
                                       published_date=now
                                       )
            for title in tags:
                tag = Tag.create(title.strip())
                ContentTag.create(question.id, tag.id)
            return HttpResponseRedirect(f'/blogs/{question.id}')
        return render(request, 'blogs/add_question.html', {'form': AddQuestionForm()})
    return render(request, 'blogs/add_question.html', {'form': AddQuestionForm()})


# def ajaxsubmit(request):
#     ret = {'status': True, 'error': None, 'data': None}
#     if (request.method == 'GET'):
#         #form = CommentForm(request.GET)
#         try:
#             content = request.GET.get('content')
#             username = request.GET.get('username')
#             postId = request.GET.get('postId')
#             print(content)
#             print(username)
#             print(postId)
#             #if form.is_valid():
#             comment = Comment.objects.create(content=content,
#                                             username=username,
#                                             postId=postId
#                                            )
#             #comment = Comment.objects.create()
#             #comment.username = username
#             #comment.content = content
#             #comment.postId = postId
#             #comment.save()
#
#             return render(request, 'blogs/index.html')
#             return HttpResponseRedirect(f'/blogs/{postId}')
#         except Exception as e:
#                 ret['status'] = False
#                 ret['error'] = 'error request'
#
#     return render(request, 'blogs/post.html', locals())


# def login(request):
#     if (request.method == 'POST'):
#         login_form = LoginForm(request.POST)

#         if login_form.is_valid():
#             username = login_form.cleaned_data['username']
#             password = login_form.cleaned_data['password']


#             userinfo = User.objects.get(username=username)  #get all info of user

#             #current_user = request.user admin user
#             #print(userinfo.email)


#             user = User.objects.filter(username__exact = username,password__exact = password)
#             print(user)
#             if user:

#                 request.session['username'] = userinfo.username
#                 request.session['useremail'] = userinfo.email
#                 request.session.set_expiry(600)
#                 return HttpResponseRedirect('/blogs')
#             else:
#                 error = 'Username is not right or password is not right!'
#                 return render(request,'blogs/login.html', {'form': LoginForm(), 'error': error})

#         return render(request, 'blogs/login.html', locals())

#     login_form = LoginForm()
#     return render(request, 'blogs/login.html', {'form': login_form, 'message': ''})

def manage(request):
    if request.method == 'POST':
        manage_form = ManageForm(request.POST)

        if manage_form.is_valid():
            newpassword = request.POST['newpassword']
            renewpassword = request.POST['renewpassword']

            latest_post_list = sorted(User.objects.all(), key=lambda p: (p.score, p.published_date.toordinal()
                                                                             if p.published_date else 0), reverse=True)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['userid'] = user.id
                request.session['username'] = user.username
                request.session['useremail'] = user.email
                request.session.set_expiry(600)
                return HttpResponseRedirect('/blogs')

            else:
                error = 'Username or password is not right!'
                return render(request,'blogs/login.html', {'form': LoginForm(), 'error': error})

        return render(request, 'blogs/login.html', locals())

    manage_form = ManageForm()
    return render(request, 'blogs/login.html', {'form': manage_form, 'message': ''})

def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['userid'] = user.id
                request.session['username'] = user.username
                request.session['useremail'] = user.email
                request.session.set_expiry(600)
                return HttpResponseRedirect('/blogs')
                
            else:
                error = 'Username or password is not right!'
                return render(request,'blogs/login.html', {'form': LoginForm(), 'error': error})

        return render(request, 'blogs/login.html', locals())

    login_form = LoginForm() 
    return render(request, 'blogs/login.html', {'form': login_form, 'message': ''})     

# def register(request):
#     if (request.method == 'POST'):
#         register_form = RegisterForm(request.POST)
#         # message = "Please check the information"
#         if register_form.is_valid():
#             username = register_form.cleaned_data['username']
#             email = register_form.cleaned_data['email']
#             password = register_form.cleaned_data['password']
#             repassword = register_form.cleaned_data['repassword']

#             if password != repassword:
#                 password_message = 'password does not match!'
#                 return render(request, 'blogs/register.html', {'form': RegisterForm(), 'password_message': password_message})

#             same_name_user = User.objects.filter(username=username)
#             if same_name_user:
#                 user_name_message = 'Username already exists!'
#                 return render(request, 'blogs/register.html', {'form': RegisterForm(), 'user_name_message': user_name_message})
#             same_email_user = User.objects.filter(email=email)
#             if same_email_user:
#                 email_message = 'Email already exists!'
#                 return render(request, 'blogs/register.html', {'form': RegisterForm(), 'email_message': email_message})

#             new_user = User.objects.create()
#             new_user.username = username
#             new_user.email = email
#             new_user.password = password
#             new_user.save()

#             # message = 'Registered Successfully!'

#             # return redirect('/login/')
#             return render_to_response("blogs/login.html")
#         else:
#             email_message = 'Invalid input!'
#             return HttpResponseRedirect('/blogs/register/', {'form': RegisterForm(), 'email_message': email_message})


#     register_form = RegisterForm()
#     return render(request, 'blogs/register.html', {'form': register_form, 'message': ''})

def register(request):
    if (request.method == 'POST'):
        register_form = RegisterForm(request.POST)
        # message = "Please check the information"
        if register_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']            
            email = request.POST['email']

            if password != request.POST['repassword']:
                password_message = 'password does not match!'
                return render(request, 'blogs/register.html', {'form': RegisterForm(), 'password_message': password_message})

            if User.objects.filter(username=username).exists():
                user_name_message = 'Username already exists!'
                return render(request, 'blogs/register.html', {'form': RegisterForm(), 'user_name_message': user_name_message})
            
            if User.objects.filter(email=email).exists():
                email_message = 'Email already exists!'
                return render(request, 'blogs/register.html', {'form': RegisterForm(), 'email_message': email_message})

            User.objects.create_user(username,email,password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = user.username
                request.session['useremail'] = user.email
                request.session.set_expiry(600)
                return HttpResponseRedirect('/blogs')
            # message = 'Registered Successfully!'
            # return render_to_response("blogs/login.html")
        else:
            email_message = 'Invalid input!'
            return HttpResponseRedirect('/blogs/register/', {'form': RegisterForm(), 'email_message': email_message})

    register_form = RegisterForm()
    return render(request, 'blogs/register.html', {'form': register_form, 'message': ''})


# def post(request):
#     return render(request, 'blogs/post.html', locals())

# def comment(request):
#     return render(request, 'blogs/comment.html', locals())


def logout_view(request):
    try:
        logout(request)
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/blogs/login/')


@login_required
def vote(request):
    if (request.method == 'GET'):
        data = request.GET
        #isvote = data.get('vote')
        isvote  = 1
        comment_id = int(data.get('commentid'))
        comment = get_object_or_404(Comment,id = comment_id)
        postid = int(data.get('postid'))
        hasvote  = Vote.objects.filter(content=comment, user=request.user).exists()
        valuevote  = Vote.objects.filter(content=comment, user=request.user)
        print("what is valuevote:")
        print(valuevote)
        initialvalue = 0
        for vote in valuevote:
            if (comment_id == vote.content.id):
                print('value:')
                vote.value += isvote
                initialvalue = vote.value
            print('commentID:')
            print(vote.content.id)
            print(vote.user)
            print(vote.value)
        print(initialvalue)


        if (hasvote):
            return HttpResponse("You have voted")
        else:

            voteinfo = Vote.objects.create(
                content = comment,
                user = request.user,
                value = initialvalue
            )

            print(voteinfo)

            valuevote  = Vote.objects.filter(content=comment, user=request.user)
            print("what is it?")
            print(voteinfo)

            context = {}
            for vote in valuevote:
                if (comment_id == vote.content.id):
                    context = {
                            'comment_id': vote.content.id,
                            'user': vote.user.username,
                            'value': vote.value

                        }
            print("context是啥：")
            print(context)

            return HttpResponse("Done")


