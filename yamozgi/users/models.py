from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from arena.models import Category

from .managers import CustomUserManager
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from django.core.files.storage import FileSystemStorage


class CustomUser(AbstractBaseUser):
    login = models.CharField(
        "имя пользователя",
        max_length=13,
        help_text="Максимальная длина 13 символов",
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
        blank=True,
    )

    avatar = models.ImageField(
        default='null',
        upload_to="uploads/%Y/%m",
        verbose_name='аватар',
    )

    @property
    def get_img(self):
        return get_thumbnail(self.avatar, "300x300", crop="center", quality=51)

    def image_tmb(self):
        if self.upload:
            return mark_safe(f'<img src="{self.get_img.url}">')
        return mark_safe('<img src="..\static_dev\homepage\img\me.png">')

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_self = CustomUser.objects.get(pk=self.pk)
            if old_self.avatar and self.avatar != old_self.avatar:
                old_self.avatar.delete(False)
        return super(CustomUser, self).save(*args, **kwargs)
    count_of_battles = models.IntegerField(
        "количество битв", null=True, blank=True
    )
    count_of_wins = models.IntegerField(
        "количество побед", null=True, blank=True
    )
    count_of_questions = models.IntegerField(
        "количество созданных вопросов",
        null=True,
        blank=True,
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
