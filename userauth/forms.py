from django import forms
from .models import Task


class Data(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
