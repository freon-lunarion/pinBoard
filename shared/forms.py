from shared.models import *
from django.shortcuts import get_object_or_404
from django import forms

class UpdateUserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)