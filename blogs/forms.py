import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from shared.models import *
from django.shortcuts import get_object_or_404
from django import forms
from tinymce.widgets import TinyMCE

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
    publish = forms.BooleanField(required=False, widget=forms.CheckboxInput)


