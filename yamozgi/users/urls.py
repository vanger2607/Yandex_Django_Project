from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path(
        "profile",
        views.Profile.as_view(),
        name="profile",
    ),
    path(
        "signin",
        views.SignIn.as_view(),
        name="signin",
    ),
    path(
        "signup",
        views.SignUp.as_view(),
        name="signup",
    ),
    path(
        "logout",
        views.LogoutUser.as_view(),
        name="logout",
    ),
    path(
        "change_password",
        views.ChangePassword.as_view(),
        name="change_password",
    ),
    path(
        "change_password_done",
        views.ChangePasswordDone.as_view(),
        name="changed_password_done",
    ),
    path(
        "reset_password",
        views.ResetPassword.as_view(),
        name="reset_password",
    ),
    path(
        "reset_password_done",
        views.ResetPasswordDone.as_view(),
        name="reset_password_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirm.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        views.PasswordResetComplete.as_view(),
        name="password_reset_complete",
    ),
]
