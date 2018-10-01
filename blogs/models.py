import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from shared.models import *
from django.shortcuts import get_object_or_404
from django import forms

# Create your models here.

class Post(Content):
    title = models.CharField(max_length=150)
    kind = models.CharField(max_length=20, default='Post')
    is_pinned = models.BooleanField(default=False)
    pin_board = models.ForeignKey(PinBoard, on_delete=models.CASCADE, default=None, blank=True, null=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def pinned(self, moderator, is_pinned=True):
        if moderator.is_superuser:
            self.is_pinned = is_pinned
            self.operator = moderator
            self.save()

    def is_favorite_of(self, user):
        is_favorite = UserFavorite.objects.filter(user=user, post=self)
        return True if is_favorite else False

    def __str__(self):
        """String for representing the Post object."""
        return f'{self.title}'


class Comment(Content):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.detail}'

    def publish(self):
        self.published_date = timezone.now()
        self.save()


# class LiveQuestionSession(Content):
#     title = models.CharField(max_length=150)
#     begin_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#
#     def __str__(self):
#         return self.title
#
#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()


class QnaQuestion(Content):
    title = models.CharField(max_length=150)
    # is_live_question = models.BooleanField(default=False)
    # parent = models.ForeignKey(LiveQuestionSession, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.title}'

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class QnaAnswer(Content):
    is_correct = models.BooleanField(default=False)
    parent = models.ForeignKey(QnaQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.detail}'

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class UserFavorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    class Meta:
        unique_together = ("post", "user")

    @staticmethod
    def create(post_id, user_id):
        post = get_object_or_404(Post, id=post_id)
        user = get_object_or_404(User, id=user_id)
        return UserFavorite.objects.create(post=post, user=user)


class User():
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)



class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="repassword", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(label='capcha')
