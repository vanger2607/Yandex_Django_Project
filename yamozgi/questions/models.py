from django.db import models
from django.utils import timezone

from arena.models import Category
from users.models import CustomUser


class Question(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    question_text = models.TextField(max_length=250)

    question_choice1 = models.TextField(max_length=250)
    question_choice2 = models.TextField(max_length=250)
    question_choice3 = models.TextField(max_length=250)
    question_choice4 = models.TextField(max_length=250)

    time_to_answer = models.PositiveIntegerField()
    is_approved = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Question, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
