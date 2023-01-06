from django.http import Http404
from django.db.models import F

from users.models import CustomUser
from questions.models import Question
from .models import Challenge, Battle


def context_for_battle_view(request):
    """функция на вход получает request,
    делает запросы к бд
    и возвращает список вызовов (challenges), брошенных текущему пользователю,
    список вызовов брошенных текущим пользователем (my_challenges),
    список текущих игр (battles)"""

    """проверка на существование user.id"""
    if request.user and request.user.id:
        user_id = request.user.id
    else:
        raise Http404

    """получаю список вызовов брошенных текущиму пользователю +
    + никнеймы и аватары пользователей, которые бросили вызов"""
    challenges = list(
        (
            Challenge.objects.filter(player_recieved_id=request.user)
            .select_related("player_sent_id")
            .values(
                login=F("player_sent_id__login"),
                avatar=F("player_sent_id__avatar"),
                sent_id=F("player_sent_id"),
            )
        )
    )

    """получаю список вызовов брошенных текущим пользователем +
    + никнеймы и аватары пользователей, которые получили вызов"""
    my_challenges = list(
        (
            Challenge.objects.filter(player_sent_id=request.user)
            .select_related("player_recieved_id")
            .values(
                login=F("player_recieved_id__login"),
                avatar=F("player_recieved_id__avatar"),
                recieved_id=F("player_recieved_id"),
            )
        )
    )

    """получаю списки текущих игр + никнеймы и аватары пользователей,
    против которых идет игра(сначала получаю список игр,
    где id текущего пользователя равен player_1_id,
    потом player_2_id, после складываю эти списки
    в переменную battles)"""
    battles_1 = list(
        Battle.objects.filter(player_1_id=user_id)
        .select_related("player_2_id")
        .values(
            "id",
            login=F("player_2_id__login"),
            avatar=F("player_2_id__avatar"),
            sent_id=F("player_2_id"),
        )
    )
    battles_2 = list(
        Battle.objects.filter(player_2_id=user_id)
        .select_related("player_1_id")
        .values(
            "id",
            login=F("player_1_id__login"),
            avatar=F("player_1_id__avatar"),
            sent_id=F("player_1_id"),
        )
    )
    battles = battles_1 + battles_2
    return challenges, my_challenges, battles
