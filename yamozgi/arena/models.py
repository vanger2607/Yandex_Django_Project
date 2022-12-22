from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "категория вопроса"
        verbose_name_plural = "категории вопросов"

    def __str__(self):
        return self.name
