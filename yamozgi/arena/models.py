from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "категория вопроса"
        verbose_name_plural = "категории вопросов"
