from .forms import *
from .models import Post, Comment, QnaQuestion, QnaAnswer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,render_to_response
from django.views import generic
import json, re
from django.utils.decorators import method_decorator

# Render content of posts
class PostView(generic.DetailView):
    model = Content
    template_name = 'blogs/post.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk', "-1")
        return super(PostView, self).dispatch(request, *args, **kwargs)

    # content: post, comments (list), comment_form, users
    def get_context_data(self, **kwargs):
        content = get_object_or_404(Content, id=self.pk)
        context = super(PostView, self).get_context_data(**kwargs)
        post_res = Post.objects.all().filter(id=content.id)

        # If it is not a question (article, image, youtube)
        if post_res.count() == 1:
            post = post_res[0]
            context['post'] = post
            context['comments'] = sorted(Comment.objects.filter(parent=post),
                                         key=lambda x: (x.score, -x.published_date.timestamp() if x.published_date
                                         else 0), reverse=True)

            context['comment_form'] = CommentForm()

        # If it is a question
        else:
            question = get_object_or_404(QnaQuestion, id=self.pk)
            context['post'] = question
            context['comments'] = question.answers
            context['comment_form'] = CommentForm()

        context['users'] = sorted(UserProfile.objects.all(), key=lambda x: (-x.score, x.user.username))[:10]

        return context

    # Create comments / answers
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        # Create comments / answers
        if form.is_valid():
            # If it is not a question
            if form.cleaned_data['comment_kind'] != 'Question':
                post = get_object_or_404(Post, id=self.pk)
                now = timezone.now().strftime("%Y-%m-%d %H:%M")
                Comment.objects.create(parent=post,
                                    detail=form.cleaned_data['comment_detail'],
                                    author= request.user,
                                    published_date=now)
            # If it is a question
            else:
                question = get_object_or_404(QnaQuestion, id=self.pk)
                # user = form.cleaned_data['comment_user']
                now = timezone.now().strftime("%Y-%m-%d %H:%M")
                QnaAnswer.objects.create(parent=question,
                                       detail=form.cleaned_data['comment_detail'],
                                       author=request.user,
                                       published_date=now)
        return HttpResponseRedirect(f'/blogs/{self.pk}')

    # Set Correct Answer for QnaAnswer
    @method_decorator(login_required)
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if 'action' in data.keys():
            if data['action'] == 'SetCorrectAnswer':
                question = QnaAnswer.objects.get(id=data['answer_id'])
                question.set_correct()
                return JsonResponse({'score': question.score})
        return HttpResponseRedirect(f'/blogs/{self.pk}')

# Render index page, supporting search by tags and search by title
@login_required
def index(request):

    # Search by tags
    if 'tags' in request.GET:
        tags = request.GET['tags'].split(',')
        contents = set([rec.id for rec in Content.objects.all()])
        for tag in tags:
            if tag.strip() == '':
                continue
            contents &= set([rec.content.id for rec in ContentTag.objects.filter(tag__title__iexact=tag.strip())])
        res = []
        for content in contents:
            post_que = Post.objects.filter(id=content)
            if post_que.count() == 1:
                res.append(Post.objects.get(id=content))
            else:
                question_que = QnaQuestion.objects.filter(id=content)
                if question_que.count() == 1:
                    res.append(QnaQuestion.objects.get(id=content))
        latest_post_list = sorted(res, key=lambda x: (x.score, x.published_date.timestamp()), reverse=True)

    # Search by title and kind
    elif 'title' in request.GET:
        words = request.GET['title'].strip().split(' ')
        contents = [rec for rec in Post.objects.all()] + [rec for rec in QnaQuestion.objects.all()]
        res = []
        for content in contents:
            hit = True
            for word in words:
                m = re.compile(r'\b%s\b' % word, re.IGNORECASE)
                if not m.search(content.title) and word.lower() != content.kind.lower():
                    hit = False
                    continue
            if hit:
                res.append(content)
        latest_post_list = sorted(res, key=lambda x: (x.score, x.create_time.timestamp()), reverse=True)

    # Index page
    else:
        latest_post_list = sorted([p for p in Post.objects.all()] + [q for q in QnaQuestion.objects.all()],
                              key=lambda p: (p.score, p.published_date.timestamp() if p.published_date else 0), reverse=True)

    context = {
        'latest_post_list': latest_post_list,
        'users': sorted(UserProfile.objects.all(), key=lambda x: (-x.score, x.user.username))[:10]
    }

    return render(request, 'blogs/index.html', context=context)

# Create article post
@login_required
def create_article_post(request):
    if (request.method == 'POST'):
        form = AddPostForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            tags = form.cleaned_data['tags'].split(',')
            post = Post.objects.create(title=form.cleaned_data['title'],
                                is_pinned=False,
                                pin_board=None,
                                operator=None,
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
            return HttpResponseRedirect(f'/blogs/{post.id}')
    return render(request, 'blogs/add_post.html', {
        'form': AddPostForm(),
        'users': sorted(UserProfile.objects.all(), key=lambda x: (-x.score, x.user.username))[:10]
    })

# Create image post
@login_required
def create_image_post(request):
    if (request.method == 'POST'):
        form = AddImageForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            tags = form.cleaned_data['tags'].split(',')
            post = Post.objects.create(title=form.cleaned_data['title'],
                                is_pinned=False,
                                pin_board=None,
                                operator=None,
                                kind='Image',
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
            return HttpResponseRedirect(f'/blogs/{post.id}')
    return HttpResponseRedirect(f'/blogs/')

# Create youtube post
@login_required
def create_youtube_post(request):
    if (request.method == 'POST'):
        form = AddImageForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            tags = form.cleaned_data['tags'].split(',')
            detail = form.cleaned_data['detail']
            if 'v=' in detail:
                m = re.compile(r'v=([_\w]+)')
                detail = m.findall(detail)[0]
            post = Post.objects.create(title=form.cleaned_data['title'],
                                is_pinned=False,
                                pin_board=None,
                                operator=None,
                                kind='Youtube',
                                detail=detail,
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
            return HttpResponseRedirect(f'/blogs/{post.id}')
    return HttpResponseRedirect(f'/blogs/')

# Create question
@login_required
def create_question(request):
    if (request.method == 'POST'):
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            now = timezone.now().strftime("%Y-%m-%d %H:%M")
            tags = form.cleaned_data['tags'].split(',')
            question = QnaQuestion.objects.create(title=form.cleaned_data['title'],
                                       detail=form.cleaned_data['detail'],
                                       author=request.user,
                                       published_date=now
                                       )
            for title in tags:
                if title.strip() == '':
                    continue
                tag = Tag.create(title.strip())
                ContentTag.create(question.id, tag.id)
            return HttpResponseRedirect(f'/blogs/{question.id}')
    return render(request, 'blogs/add_question.html', {
        'form': AddQuestionForm(),
        'users': sorted(UserProfile.objects.all(), key=lambda x: (-x.score, x.user.username))[:10]
    })

# API: Pin a post or a question
@login_required
def pin(request, pk):
    if (request.method == 'PUT'):
        if not request.user.is_superuser:
            return HttpResponse(status=403)
        post_res = Post.objects.filter(id=pk)

        # If it is a post
        if post_res.count() == 1:
            post = Post.objects.get(id=pk)
            post.is_pinned = True
            post.operator = request.user
            post.save()

        # If it is a question
        else:
            question = QnaQuestion.objects.get(id=pk)
            question.is_pinned = True
            question.operator = request.user
            question.save()
        return HttpResponse(status=200)

# API: Unpin a post or a question
@login_required
def unpin(request, pk):
    if (request.method == 'PUT'):
        if not request.user.is_superuser:
            return HttpResponse(status=403)
        post_res = Post.objects.filter(id=pk)

        # If it is a post
        if post_res.count() == 1:
            post = Post.objects.get(id=pk)
            post.is_pinned = False
            post.operator = request.user
            post.save()

        # If it is a question
        else:
            question = QnaQuestion.objects.get(id=pk)
            question.is_pinned = False
            question.operator = request.user
            question.save()
        return HttpResponse(status=200)

# Log in
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
                request.session['password'] = user.password
                request.session['avatar'] = user.userprofile.avatar
                print(user.userprofile.avatar)
                request.session.set_expiry(6000)
                return HttpResponseRedirect('/blogs')
                
            else:
                error = 'Username or password is not right!'
                return render(request,'blogs/login.html', {'form': LoginForm(), 'error': error})

        return render(request, 'blogs/login.html', locals())

    login_form = LoginForm() 
    return render(request, 'blogs/login.html', {'form': login_form, 'message': ''})

# Register
def register(request):
    if (request.method == 'POST'):
        register_form = RegisterForm(request.POST)
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
        else:
            email_message = 'Invalid input!'
            return HttpResponseRedirect('/blogs/register/', {'form': RegisterForm(), 'email_message': email_message})

    register_form = RegisterForm()
    return render(request, 'blogs/register.html', {'form': register_form, 'message': ''})

# Log out
def logout_view(request):
    try:
        logout(request)
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect('/blogs/login/')

# API: Reset password
@login_required
def reset(request):
    if (request.method == 'PUT'):
        data = json.loads(request.body)
        newpassword = data['newpassword']
        renewpassword = data['renewpassword']
        if (newpassword != renewpassword):
           return HttpResponse("Password is not matched", status=400)
        user = UserProfile.objects.get(user__id=request.user.id).user
        user.set_password(renewpassword)
        user.save()
        return HttpResponse('Done', status=200)
