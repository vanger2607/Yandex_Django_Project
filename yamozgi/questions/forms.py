from django import forms
# from django.forms import TextInput

from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = []
