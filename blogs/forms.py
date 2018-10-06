import datetime
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from shared.models import *
from django.shortcuts import get_object_or_404
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128,
                               widget=forms.TextInput(attrs={
                                   # 'class': 'form-control',
                                   'placeholder': 'Username',
                                   'id': 'Lastname'
                               }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                 # 'class': 'form-control',
                                 'placeholder': 'Email',
                                 'oninput': 'OnInput (event)',
                                 'id': 'Email'
                             }))
    password = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    # 'class': 'form-control',
                                    'placeholder': 'Password',
                                    'id': 'password'
                                }))
    repassword = forms.CharField(max_length=256,
                                widget=forms.PasswordInput(attrs={
                                    # 'class': 'form-control',
                                    'placeholder': 'Confirm password',
                                    'id': 'repassword'
                                }))
    # captcha = CaptchaField(label='capcha')

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField(label='capcha')