from django.urls import path

from . import views

app_name = "duels"

urlpatterns = [
    path(
        "battles",
        views.BattleView.as_view(),
        name="battles",
    ),
    path(
        "make_challenge",
        views.UserList.as_view(),
        name="userlist",
    ),
    path(
        "question",
        views.QuestionView.as_view(),
        name="question",
    ),
    path(
        "question-api",
        views.question_api,
        name="question-api",
    ),
    path(
        "challenge-api",
        views.challenge_to_other_api,
        name="challenge-api",
    ),
    path(
        "decline-challenge-api",
        views.decline_challenge_api,
        name="decline-challenge-api",
    ),
    path(
        "accept-challenge-api",
        views.accept_challenge_api,
        name="accept-challenge-api",
    ),
    path(
        "decline-my-challenge-api",
        views.decline_my_challenge_api,
        name="decline-my-challenge-api",
    ),
]
