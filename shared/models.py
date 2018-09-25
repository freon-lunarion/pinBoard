from django.db import models
from django.utils import timezone
import datetime
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import get_object_or_404

# Create your models here.

class User(AbstractUser):

    def __str__(self):
        return self.username

    @staticmethod
    def create_student(username, password, email=''):
        return User.objects.create_user(username, email, password)

    @staticmethod
    def create_moderator(username, password, email=''):
        return User.objects.create_superuser(username, email, password)


class CoursePinBoard(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @staticmethod
    def create(title, creator, detail=''):
        return CoursePinBoard.objects.create(title=title, detail=detail, creator=creator)


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

    @property
    def is_published_recently(self):
        return self.create_time >= timezone.now() - datetime.timedelta(days=1)


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    @staticmethod
    def create(title):
        return Tag.objects.create(title=title)


class ContentTag(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)

    class Meta:
        unique_together = ("content", "tag")

    @staticmethod
    def create(content_id, tag_id):
        content = get_object_or_404(Content, id=content_id)
        tag = get_object_or_404(Tag, id=tag_id)
        return ContentTag.objects.create(content=content, tag=tag)


class Vote(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("content", "user")

    @staticmethod
    def create(content_id, user_id, value):
        content = get_object_or_404(Content, id=content_id)
        user = get_object_or_404(User, id=user_id)
        return Vote.objects.create(content=content, user=user, value=value)