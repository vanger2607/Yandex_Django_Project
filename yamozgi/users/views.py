from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.auth.views import LoginView

from .forms import ProfileForm, SignInForm, SignUpForm


class Profile(TemplateView, FormView):
    template_name = "users/profile.html"
    form_class = ProfileForm


class SignIn(LoginView):
    form_class = SignInForm
    template_name = "users/signin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "users/signup.html"
