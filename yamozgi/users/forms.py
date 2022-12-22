from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.core.exceptions import ValidationError
from django.forms import EmailInput, SelectDateWidget, TextInput

from .models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["login", "birthday", "avatar"]
        widgets = {
            "login": TextInput(
                attrs={
                    "class": "light-pink-input inputs__input",
                },
            ),
            "birthday": SelectDateWidget(
                years=range(1940, 2014),
                attrs={
                    "class": "light-pink-input date-input",
                },
            ),
        }


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label=("Пароль:"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "class": "form-field light-pink-input",
            }
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-field light-pink-input"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["email", "login"]
        CustomUser.login.label_classes = "form-label"
        widgets = {
            "login": TextInput(
                attrs={
                    "class": "form-field light-pink-input",
                    "placeholder": "nickname",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-field light-pink-input",
                    "placeholder": "example@mail.ru",
                }
            ),
            "password2": forms.PasswordInput(
                attrs={
                    "class": "form-field light-pink-input",
                }
            ),
        }


FIELD_NAME_MAPPING = {"username": "email"}


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        label="Почта",
        widget=(
            forms.EmailInput(
                attrs={
                    "class": "form-field light-pink-input",
                    "autofocus": True,
                }
            )
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-field light-pink-input",
                "autocomplete": "current-password",
            }
        ),
    )

    class Meta:
        model = CustomUser
        password = CustomUser.password.field.name

        fields = (password,)

        labels = {
            password: "Пароль",
        }

        widgets = {
            password: forms.PasswordInput(
                attrs={
                    "class": "form-field light-pink-input",
                    "required": True,
                }
            ),
        }


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="ведите новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "новый пароль",
                "class": "form-field light-pink-input",
                "autofocus": True,
            }
        ),
    )
    new_password2 = forms.CharField(
        label="повторите новый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "повторите пароль",
                "class": "form-field light-pink-input",
            }
        ),
    )


class MyPasswordChangeForm(MySetPasswordForm):
    error_messages = {
        **SetPasswordForm.error_messages,
        "password_incorrect": (
            "Ваш старый пароль был введен неправильно," "попробуйте еще раз"
        ),
    }
    old_password = forms.CharField(
        label="старый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "class": "form-field light-pink-input",
            }
        ),
    )

    field_order = ["old_password", "new_password1", "new_password2"]

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages["password_incorrect"],
                code="password_incorrect",
            )
        return old_password


class MyResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label=("Почта"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-field light-pink-input",
            }
        ),
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="ведите новый пароль",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "новый пароль",
                "class": "form-field light-pink-input",
                "autofocus": True,
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="повторите новый пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "повторите пароль",
                "class": "form-field light-pink-input",
            }
        ),
    )
