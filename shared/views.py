from .models import *
from blogs.models import Post,QnaQuestion
from quiz.models import QuizBank
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
import json
# Create your views here.

# API: give score to a post. Url: /vote/
@login_required
def vote(request, pk):
    if (request.method == 'PUT'):
        data = json.loads(request.body)
        vote =  data['vote']
        return JsonResponse({'score': Vote.vote(pk, request.user.id, vote)})
    if (request.method == 'GET'):
        return JsonResponse({'exist': Vote.exist(pk, request.user.id)})

# API: modify user avatar. Url: /user_avatar/
@login_required
def user_avatar(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        request.user.userprofile.avatar = data['avatar']
        request.user.userprofile.save()
        request.session['avatar'] = data['avatar']
        return JsonResponse({'message': 'Succeed'})

# Render user profile page. Url: /user/<user_id>
@login_required
def user_profile(request, pk):

    profile = UserProfile.objects.get(pk=pk)
    article = Post.objects.filter(author=profile.user,kind='Post')
    images = Post.objects.filter(author=profile.user,kind='Image')
    videos = Post.objects.filter(author=profile.user, kind='Youtube')
    qna = QnaQuestion.objects.filter(author=profile.user,kind='Question')
    quiz = QuizBank.objects.filter(creator=profile.user)

    context = {
        'profile' : profile,
        'article' : article,
        'images' : images,
        'videos': videos,
        'qna' : qna,
        'quiz' : quiz,
        'users' : sorted(UserProfile.objects.all(), key=lambda x: (-x.score, x.user.username))[:10]
    }
    
    return render(request,'shared/user_profile.html',context=context)

# API: save post as favorite. Url: /<post_id>/like/
@login_required
def user_like(request, pk):
    if request.method == 'PUT':
        UserFavorite.create(pk, request.user.id)
        return JsonResponse({'message': 'Succeed'})

# API: remove post from favorite. Url: /<post_id>/unlike/
@login_required
def user_unlike(request, pk):
    if request.method == 'PUT':
        UserFavorite.objects.get(content__id=pk, user=request.user).delete()
        return JsonResponse({'message': 'Succeed'})

# API: Get user data for leaderboard. Url: /user/
@login_required
def user(request):
    if request.method == 'GET':
        users = []
        for user in sorted(UserProfile.objects.all(), key=lambda x: (-x.score, x.user.username))[:10]:
            user_json = {}
            user_json['avatar'] = user.avatar
            user_json['id'] = user.id
            user_json['score'] = user.score
            user_json['rank'] = user.rank
            user_json['total_answer_num'] = user.total_answer_num
            user_json['correct_answer_num'] = user.correct_answer_num
            user_json['correct_answer_percentage'] = user.correct_answer_percentage
            user_json['username'] = user.user.username
            user_json['email'] = user.user.email
            users.append(user_json)
        return JsonResponse({'users': users})