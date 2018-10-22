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
                                   'placeholder': 'username',
                                   'id': 'Lastname'
                               }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                 'placeholder': 'email',
                                 'oninput': 'OnInput (event)',
                                 'id': 'Email'
                             }))
    password = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'password',
                                    'id': 'password'
                                }))
    repassword = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'confirm password',
                                    'id': 'repassword'
                                }))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'username',
                                   'id': 'username'
                               }))
    password = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'password',
                                    'id': 'password'
                                }))

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=128)
    detail = forms.CharField(required=False, widget=forms.Textarea)
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'tags',
        'placeholder': 'use , to separate tags'
    }))

class AddQuestionForm(forms.Form):
    title = forms.CharField(max_length=128)
    detail = forms.CharField(required=False, widget=forms.Textarea)
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'tags',
        'placeholder': 'use , to separate tags'
    }))

class AddImageForm(forms.Form):
    title = forms.CharField(max_length=128)
    image = forms.CharField(required=False, widget=forms.FileInput(attrs={
        'type': 'file',
        'id': 'picker'
    }))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'tags',
        'placeholder': 'use , to separate tags'
    }))
    detail = forms.CharField(widget=forms.TextInput(attrs={
        'id': 'detail',
        'type': 'hidden'
    }))

class CommentForm(forms.Form):
    comment_detail = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'id': "comment_detail",
        'style': 'height: 300px'
    }))
    comment_kind = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'hidden',
        'id': 'comment_kind'
    }))
