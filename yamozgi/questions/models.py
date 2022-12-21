from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from core.models import CoreSave
from users.models import CustomUser


class Category(CoreSave):
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "категория вопроса"
        verbose_name_plural = "категории вопросов"


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

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Question, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
