from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from arena.models import Category
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    login = models.CharField(
        "имя пользователя",
        max_length=30,
        help_text="Максимальная длина 30 символов",
    )
    email = models.EmailField(
        "почта",
        max_length=150,
        unique=True,
        help_text="Максимальная длина 150 символов",
    )

    birthday = models.DateField(
        "день рождения",
        blank=True,
        null=True,
        help_text="Укажите дату рождения",
    )

    best_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="лучшая категория",
        null=True,
    )

    count_of_battles = models.IntegerField("количество битв", null=True)
    count_of_wins = models.IntegerField("количество побед", null=True)
    count_of_questions = models.IntegerField(
        "количество созданных вопросов", null=True
    )

    is_staff = models.BooleanField("сотрудник", default=False)
    is_superuser = models.BooleanField("админ", default=False)
    is_active = models.BooleanField("активный пользователь", default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["login", "password"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.login

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
