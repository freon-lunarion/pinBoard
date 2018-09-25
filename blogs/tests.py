from django.test import TestCase
from .models import *
from shared.models import *
from django.shortcuts import get_object_or_404

# Create your tests here.

class ModelTestCase(TestCase):

    def setUp(self):
        student1 = User.create_student(username='student1', password='student1')
        # student2 = BlogsUser.new_user(username='student2', password='student2')
        moderator = User.create_moderator(username='admin', password='admin')
        pinboard = CoursePinBoard.create(title="COMP9323", creator=moderator)
        p1 = Post.objects.create(title="Hello", detail="World", author=student1, pin_board=pinboard)
        # p2 = student2.create_post(title="Hello", detail="Beauty", pinboard=pinboard)
        # c1 = student1.create_comment(parent=p1, detail="Go")
        # student2.vote(content=p1, value=1)
        Vote.vote(p1.id, student1.id, -1)

    def test_get_posts(self):
        # post = Post.objects.get(id=1)
        # comment = Comment.objects.all()
        # for post in Post.objects.filter(pinboard=pinboard):
        #     print(post.score)
        vote = get_object_or_404(Vote, content=1)
        vote1 = get_object_or_404(Vote, user=1)
        print(vote.user)
        print(vote1.content)
