from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("create_question", views.CreateQuestion.as_view(), name="create",),
]
