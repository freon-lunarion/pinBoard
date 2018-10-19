from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.utils import timezone
from tinymce import models as tinymce_models
import datetime

# Create your models here.

class UserProfile(models.Model):
    # REF : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    # REF : https://stackoverflow.com/questions/6396442/add-image-avatar-field-to-users-in-django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    @property
    def score(self):
        total_score = 0
        contents = Content.objects.filter(author=self.user)
        for content in contents:
            total_score += content.score
        return total_score


    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.shared.save()

# class User(AbstractUser):

#     def __str__(self):
#         return self.username

#     @staticmethod
#     def create_student(username, password, email=''):
#         return User.objects.create_user(username, email, password)

#     @staticmethod
#     def create_moderator(username, password, email=''):
#         return User.objects.create_superuser(username, email, password)


class PinBoard(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @staticmethod
    def create(title, creator, detail=''):
        return PinBoard.objects.create(title=title, detail=detail, creator=creator)


class Content(models.Model):
    detail = tinymce_models.HTMLField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    @property
    def score(self):
        score = Vote.objects.filter(content=self).aggregate(total=Sum("value"))["total"]
        return score if score else 0
    
    @property
    def num_voter(self):
        num_voter = Vote.objects.filter(content=self).aggregate(total=Count("value"))["total"]
        return num_voter if num_voter else 0

    @property
    def is_published_recently(self):
        return self.create_time >= timezone.now() - datetime.timedelta(days=1)

    @property
    def tags(self):
        return [obj.tag.title for obj in ContentTag.objects.filter(content__exact=self)]


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
    value = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)

    @staticmethod
    def vote(content_id, user_id, value):
        content = get_object_or_404(Content, id=content_id)
        user = get_object_or_404(User, id=user_id)
        Vote.objects.create(content=content, user=user, value=value)
        return content.score

    @staticmethod
    def exist(content_id, user_id):
        content = get_object_or_404(Content, id=content_id)
        user = get_object_or_404(User, id=user_id)
        if Vote.objects.filter(content=content, user=user).exists():
            return 1
        else:
            return 0