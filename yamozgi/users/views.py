from django.views.generic import TemplateView, FormView, CreateView
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy

from .forms import (
    ProfileForm,
    SignInForm,
    SignUpForm,
    MyPasswordChangeForm,
    MyResetPasswordForm,
    MySetPasswordForm,
)


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


class ChangePassword(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy("users:changed_password_done")
    template_name = "users/change_password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "смена пароля"
        return context


class ChangePasswordDone(PasswordChangeDoneView):
    template_name = "users/change_password_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "пароль успешно сменен"
        return context


class ResetPassword(PasswordResetView):
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    form_class = MyResetPasswordForm
    success_url = reverse_lazy("users:reset_password_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "восстановление пароля"
        return context


class ResetPasswordDone(PasswordResetDoneView):
    template_name = "users/reset_password_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "смена пароля письмо отправлено"
        return context


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    form_class = MySetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "новый пароль"
        return context


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
    success_url = reverse_lazy("users:signin")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "пароль успешно изменен"
        return context
