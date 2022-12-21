from django import forms
from django.forms import TextInput, Select

from .models import Question
from arena.models import Category


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        category = forms.ModelChoiceField(
            queryset=Category.objects.all())
        fields = ["question_text", "question_choice1", "question_choice2",
                  "question_choice3", "question_choice4",
                  "category", "right_answer"]
        labels = {
            "question_text": "Вопрос:",
            "question_choice1": "Ответ 1:",
            "question_choice2": "Ответ 2:",
            "question_choice3": "Ответ 3:",
            "question_choice4": "Ответ 4:",
            "right_answer": "Верный ответ:",
            "category": "Категория:",
        }
        help_texts = {
            "right_answer": "Номер вопроса от 1 до 4",
        }
        widgets = {
            "question_text": TextInput(
                attrs={'class': 'light-pink-input inputs__input big',
                       'required': True}),
            "question_choice1": TextInput(
                attrs={'class': 'light-pink-input inputs__input',
                       'required': True}),
            "question_choice2": TextInput(
                attrs={'class': 'light-pink-input inputs__input',
                       'required': True}),
            "question_choice3": TextInput(
                attrs={'class': 'light-pink-input inputs__input',
                       'required': True}),
            "question_choice4": TextInput(
                attrs={'class': 'light-pink-input inputs__input',
                       'required': True}),
            "right_answer": TextInput(
                attrs={'class': 'light-pink-input inputs__input',
                       'required': True}),
            "category": Select(
                attrs={'class': 'light-pink-input inputs__input',
                       'required': True}),
        }
