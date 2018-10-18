import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from shared.models import *
from django.shortcuts import get_object_or_404
from django import forms
from tinymce.widgets import TinyMCE
from django.contrib.admin import widgets

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={
                                   # 'class': 'form-control',
                                   'placeholder': 'username',
                                   'id': 'Lastname'
                               }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                 # 'class': 'form-control',
                                 'placeholder': 'email',
                                 'oninput': 'OnInput (event)',
                                 'id': 'Email'
                             }))
    password = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    # 'class': 'form-control',
                                    'placeholder': 'password',
                                    'id': 'password'
                                }))
    repassword = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    # 'class': 'form-control',
                                    'placeholder': 'confirm password',
                                    'id': 'repassword'
                                }))
    # captcha = CaptchaField(label='capcha')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={
                                   # 'class': 'form-control',
                                   'placeholder': 'username',
                                   'id': 'username'
                               }))
    password = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    # 'class': 'form-control',
                                    'placeholder': 'password',
                                    'id': 'password'
                                }))
    # captcha = CaptchaField(label='capcha')


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=128)
    detail = forms.CharField(required=False, widget=forms.Textarea)
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'tags',
        'placeholder': 'use , to separate tags'
    }))
    # publish = forms.IntegerField(widget=forms.TextInput(attrs={'id': 'publish',
    #                                                            'type': 'button',
    #                                                            'checked': 'true'}))
    # publish = forms.DatetimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

class AddQuestionForm(forms.Form):
    title = forms.CharField(max_length=128)
    detail = forms.CharField(required=False, widget=forms.Textarea)
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'tags',
        'placeholder': 'use , to separate tags'
    }))

class CommentForm(forms.Form):
    comment_detail = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'id': "comment_detail",
        'style': 'height: 300px'
    }))
    comment_user = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={
        'type': 'hidden',
        'id': 'comment_user'
    }))