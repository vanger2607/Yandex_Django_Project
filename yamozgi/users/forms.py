from django import forms
from django.forms import SelectDateWidget, TextInput, EmailInput
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
