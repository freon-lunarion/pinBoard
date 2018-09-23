from django.test import TestCase
from .models import Post, Comment, Vote, Content
from django.contrib.auth.models import User

# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin', password='admin')
        p1 = Post.objects.create(title="liontitle", detail="lion", author=user)
        c1 = Comment.objects.create(parent=p1, detail="lion", author=user)
        Vote.objects.create(content=p1, author=user, value=1)
        Vote.objects.create(content=c1, author=user, value=-1)

    def test_get_posts(self):
        post = Post.objects.get(id=1)
        print(post.score)
        comment = Comment.objects.get(id=2)
        print(comment.score)