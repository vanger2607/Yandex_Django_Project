from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView

from . import forms
from users.models import CustomUser


def sign_up(request):
    template_name = "users/signup.html"
    form = forms.SignUpForm(request.POST or None)
    context = {
        "form": form,
    }

    if request.method == "POST" and form.is_valid():
        login = form.cleaned_data["login"]
        mail = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        CustomUser.objects.create_user(mail, login, password)
        return redirect("users:signin")

    return render(request, template_name, context)


class SignIn(LoginView):
    form_class = forms.SignInForm
    template_name = "users/signin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
