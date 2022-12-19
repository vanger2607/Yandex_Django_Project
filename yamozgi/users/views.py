from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from users.forms import SignUpForm, SignInForm
from users.models import CustomUser
from django.urls import reverse_lazy


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("users:signin")
    template_name = "users/signup.html"


class SignIn(LoginView):
    form_class = SignInForm
    template_name = "users/signin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
