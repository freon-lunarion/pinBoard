import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# class Pinboard(models.Model):
#     title = models.CharField(max_length=50)
#     detail = models.TextField()
#     creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title

class Content(models.Model):
    detail = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    @property
    def score(self):
        score = Vote.objects.filter(content=self).aggregate(total=Sum("value"))["total"]
        return score if score else 0

    def is_published_recently(self):
        return self.create_time >= timezone.now() - datetime.timedelta(days=1)

class Post(Content):
    title = models.CharField(max_length=150)
    is_pinned = models.BooleanField(default=False)
    # pinned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    # pinboard = models.ForeignKey(Pinboard, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

class UserFavorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Comment(Content):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.detail

class LiveQuestionSession(Content):
    title = models.CharField(max_length=150)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

class QnaQuestion(Content):
    title = models.CharField(max_length=150)
    is_live_question = models.BooleanField(default=False)
    perent = models.ForeignKey(LiveQuestionSession, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class QnaAnswer(Content):
    is_correct = models.BooleanField(default=False)
    parent = models.ForeignKey(QnaQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.detail

class Tag(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title

class ContentTag(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

class Vote(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)