from django.urls import path

from . import views

app_name = "duels"

urlpatterns = [
    path(
        "battles",
        views.Battle.as_view(),
        name="battles",
    ),
    path(
        "question",
        views.QuestionView.as_view(),
        name="question",
    ),
    path("question-api", views.QuestionAPI, name="question-api"),
]
