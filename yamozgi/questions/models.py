from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import CoreSave
from users.models import CustomUser
from arena.models import Category


class Question(CoreSave):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
    )
    question_text = models.TextField(max_length=250)

    question_choice1 = models.TextField(max_length=250)
    question_choice2 = models.TextField(max_length=250)
    question_choice3 = models.TextField(max_length=250)
    question_choice4 = models.TextField(max_length=250)

    right_answer = models.PositiveIntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        default=1,
    )
    difficulty = models.IntegerField(default=0)

    is_approved = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
