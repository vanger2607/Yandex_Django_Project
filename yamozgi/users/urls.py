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
]
