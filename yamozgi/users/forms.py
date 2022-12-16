from django import forms

from .models import CustomUser


class SignUpForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["password_confirm"] = forms.CharField(
            max_length=128,
            required=True,
            label="Подтвердите пароль",
            widget=forms.PasswordInput(attrs={"class": "form-control"}),
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
            mail: forms.EmailInput(attrs={"class": "form-control",
                                          "required": True}),
            login: forms.TextInput(attrs={"class": "form-control",
                                          "required": True}),
            password: forms.PasswordInput(
                attrs={"class": "form-control", "required": True}
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


class SignInForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields["login_or_mail"] = forms.CharField(
            required=True,
            label="Логин или почта",
            widget=forms.PasswordInput(attrs={"class": "form-control",
                                              "required": True}),
        )

    class Meta:
        model = CustomUser
        password = CustomUser.password.field.name

        fields = (password, )

        labels = {
            password: "Пароль",
        }

        widgets = {
            password: forms.PasswordInput(
                attrs={"class": "form-control", "required": True}
            ),
        }

    def clean_password_confirm(self):
        cleaned_data = super(SignInForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return cleaned_data
