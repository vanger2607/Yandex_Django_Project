from django.urls import path

from users import views

app_name = "users"
urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("signin/", views.SignIn.as_view(), name="signin"),
]
