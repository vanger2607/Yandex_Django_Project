from django.shortcuts import redirect, render

from . import forms
from users.models import CustomUser
from django.contrib.auth import authenticate, login


def sign_up(request):
    template_name = "users/signup.html"
    form = forms.SignupForm(request.POST or None)
    context = {
        "form": form,
    }

    if request.method == "POST" and form.is_valid():
        login = form.cleaned_data["login"]
        mail = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        CustomUser.objects.create_user(mail, login, password)
        return redirect("users:signup")

    return render(request, template_name, context)


def sign_in(request):
    template_name = "users/signin.html"
    form = forms.SignInForm(request.POST or None)
    context = {
        "form": form,
    }

    if request.method == "POST" and form.is_valid():
        user = form.save()
        user.refresh_from_db()

        CustomUser.objects.update_or_create(user=user)

        user.save()
        raw_password = form.cleaned_data.get("password")

        user = authenticate(username=user.username, password=raw_password)
        login(request, user)

        return redirect("homepage:home-landing")
    return render(request, template_name, context)
