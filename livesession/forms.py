from django import forms

class AddLiveQuestionSessionForm(forms.Form):
    title = forms.CharField(max_length=128)
    detail = forms.CharField(required=False, widget=forms.Textarea)
    begin_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class': '"glyphicon glyphicon-calendar"'
    }))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'class': '"glyphicon glyphicon-calendar"'
    }))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'id': 'tags',
        'placeholder': 'use , to separate tags'
    }))