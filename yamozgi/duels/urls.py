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
        "battles/<int:pk>/rounds/<int:round>",
        views.RoundChooseView.as_view(),
        name="choose_category",
    ),
    path(
        "battles/<int:pk>/rounds/<int:round>/question_pos/<int:pos>",
        views.QuestionView.as_view(),
        name="question",
    ),
    path(
        (
            "battles/<int:pk>/rounds/<int:round>/question_pos/"
            "<int:pos>/complete/user/<int:user_id>"
        ),
        views.QuestionCompleteView.as_view(),
        name="question-complete",
    ),
    path(
        "question-api-start",
        views.question_api_start,
        name="question-api-start",
    ),
    path(
        "question_api_endtime",
        views.question_api_endtime,
        name="question_api_endtime",
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
    path(
        "battles/<int:pk>",
        views.DetailBattleView.as_view(),
        name="battle_detail",
    ),
]
