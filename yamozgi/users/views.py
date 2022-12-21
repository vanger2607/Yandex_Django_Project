import os
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    LogoutView,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from django.core.files.storage import FileSystemStorage

from .forms import (
    MyPasswordChangeForm,
    MyResetPasswordForm,
    MySetPasswordForm,
    ProfileForm,
    SignInForm,
    SignUpForm,
)
from .models import CustomUser


class Profile(TemplateView, FormView):
    model = CustomUser
    template_name = "users/profile.html"
    form_class = ProfileForm

    def form_valid(self, form):
        user = self.request.user
        user.login = form.cleaned_data["login"]
        user.birthday = str(form.cleaned_data["birthday"])
        print(self.request.FILES)
        if self.request.FILES and self.request.FILES['avatar']:
            print("okkkkkkkkkkkk")
            upload = self.request.FILES["avatar"]
            print(upload.name)
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)[1:]
            print(file_url)
            if user.avatar:
                os.remove(str(user.avatar))
            user.avatar = file_url
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("ok")
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        userform = self.form_class(
            self.request.POST or None,
            initial={"login": user.login, "birthday": user.birthday},
        )
        context["form"] = userform
        return context

    def get_success_url(self, **kwargs):
        return reverse_lazy("users:profile")


class SignIn(LoginView):
    form_class = SignInForm
    template_name = "users/signin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:signin")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LogoutUser(LogoutView):
    next_page = "users:signin"


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
