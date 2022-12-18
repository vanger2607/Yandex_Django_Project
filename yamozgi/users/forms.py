from django import forms
from django.forms import SelectDateWidget, TextInput, EmailInput
from django.contrib.auth.forms import AuthenticationForm

from .models import CustomUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = {"login", "email", "birthday"}
        widgets = {
            "login": TextInput(
                attrs={
                    "class": "light-pink-input inputs__input",
                    "placeholder": "Nickname",
                },
            ),
            "email": EmailInput(
                attrs={
                    "class": "light-pink-input inputs__input  medium-input",
                    "placeholder": "Email",
                },
            ),
            "birthday": SelectDateWidget(
                years=range(1940, 2014),
                attrs={
                    "class": "light-pink-input date-input",
                },
            ),
        }


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["password_confirm"] = forms.CharField(
            max_length=128,
            required=True,
            label="Подтвердите пароль",
            widget=forms.PasswordInput(
                attrs={"class": "form-field light-pink-input"}
            ),
        )

    class Meta:
        model = CustomUser
        login = CustomUser.login.field.name
        mail = CustomUser.email.field.name
        password = CustomUser.password.field.name

        fields = (mail, login, password)

        labels = {
            mail: "Электронная почта",
            login: "Логин",
            password: "Пароль",
        }

        widgets = {
            mail: forms.EmailInput(
                attrs={
                    "class": "form-field light-pink-input",
                    "required": True,
                }
            ),
            login: forms.TextInput(
                attrs={
                    "class": "form-field light-pink-input",
                    "required": True,
                }
            ),
            password: forms.PasswordInput(
                attrs={
                    "class": "form-field light-pink-input",
                    "required": True,
                }
            ),
        }

    error_messages = {
        "password_mismatch": "Пароли не совпадают",
    }

    def clean_password_confirm(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return cleaned_data


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        label="почта или логин",
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
        label="пароль",
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
