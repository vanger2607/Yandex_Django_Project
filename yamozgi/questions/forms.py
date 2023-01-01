from django import forms
from django.forms import TextInput, Select

from .models import Question
from questions.models import Category


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    category = forms.ModelChoiceField(
        queryset=Category.objects.all().only("name"),
        empty_label=None,
        label="Категория: ",
        widget=Select(
            attrs={
                "class": "light-pink-input inputs__input",
                "required": True,
            }
        ),
    )

    class Meta:
        CHOICES = [
            ("question_choice1", "Ответ 1"),
            ("question_choice2", "Ответ 2"),
            ("question_choice3", "Ответ 3"),
            ("question_choice4", "Ответ 4"),
        ]
        model = Question

        fields = [
            "question_text",
            "question_choice1",
            "question_choice2",
            "question_choice3",
            "question_choice4",
            "right_answer",
        ]
        labels = {
            "question_text": "Вопрос:",
            "question_choice1": "Ответ 1:",
            "question_choice2": "Ответ 2:",
            "question_choice3": "Ответ 3:",
            "question_choice4": "Ответ 4:",
            "right_answer": "Верный ответ:",
        }
        help_texts = {
            "right_answer": "Номер вопроса от 1 до 4",
        }
        widgets = {
            "question_text": TextInput(
                attrs={
                    "class": "light-pink-input inputs__input big",
                    "required": True,
                }
            ),
            "question_choice1": TextInput(
                attrs={
                    "class": "light-pink-input inputs__input",
                    "required": True,
                }
            ),
            "question_choice2": TextInput(
                attrs={
                    "class": "light-pink-input inputs__input",
                    "required": True,
                }
            ),
            "question_choice3": TextInput(
                attrs={
                    "class": "light-pink-input inputs__input",
                    "required": True,
                }
            ),
            "question_choice4": TextInput(
                attrs={
                    "class": "light-pink-input inputs__input",
                    "required": True,
                }
            ),
            "right_answer": forms.RadioSelect(
                choices=CHOICES,
            ),
        }
