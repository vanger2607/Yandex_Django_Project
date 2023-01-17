import logging

from django.http import Http404
from django.db.models import F
from django.shortcuts import get_object_or_404
from .models import Challenge, Battle, Round, PlayerAnswer

logger = logging.getLogger(__name__)


def check_and_return_existence_user_id(request):
    """проверяет передала ли нам джанго pk,
    если почему-то не передала бросаем ошибку"""
    if request.user and request.user.id:
        return request.user.id
    else:
        raise Http404


def check_correct_user_in_battle(user_id, battle_id):
    """проверяет, может ли игрок находится в этой битве
    или пытается попасть в чужую и если все хорошо возвращает battle_obj
    (какой сейчас раунд и айди игроков)"""
    battle_obj = get_object_or_404(
        Battle.objects.only(
            "round_now",
            "player_1_id",
            "player_2_id",
            "is_over",
        ),
        pk=battle_id,
    )
    if not (user_id in [battle_obj.player_2_id, battle_obj.player_1_id]):
        raise Http404
    return battle_obj


def check_correct_user_in_battle_by_obj(user_id, battle_obj):
    """проверяет, может ли игрок находится в этой битве
    или пытается попасть в чужую и если все хорошо возвращает battle_obj
    (какой сейчас раунд и айди игроков)"""
    if not (user_id in [battle_obj.player_2_id, battle_obj.player_1_id]):
        raise Http404
    return battle_obj


def context_for_battle_view(request):
    """функция на вход получает request,
    делает запросы к бд
    и возвращает список вызовов (challenges), брошенных текущему пользователю,
    список вызовов брошенных текущим пользователем (my_challenges),
    список текущих игр (battles)"""

    """проверка на существование user.id"""
    user_id = check_and_return_existence_user_id(request)

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

    """получаю списки  законченных битв пользователя +
    + никнеймы и аватары пользователей, которые закончили эту битву"""
    my_ended_battles_1 = list(
        (
            Battle.objects.filter(player_1_id=user_id, is_over=True)
            .select_related("player_2_id")
            .values(
                "id",
                login=F("player_2_id__login"),
                avatar=F("player_2_id__avatar"),
                recieved_id=F("player_2_id"),
            )
        )
    )
    my_ended_battles_2 = list(
        (
            Battle.objects.filter(player_2_id=user_id, is_over=True)
            .select_related("player_1_id")
            .values(
                "id",
                login=F("player_1_id__login"),
                avatar=F("player_1_id__avatar"),
                recieved_id=F("player_1_id"),
            )
        )
    )
    my_ended_battles = my_ended_battles_1 + my_ended_battles_2
    """получаю списки текущих игр + никнеймы и аватары пользователей,
    против которых идет игра(сначала получаю список игр,
    где id текущего пользователя равен player_1_id,
    потом player_2_id, после складываю эти списки
    в переменную battles)"""
    battles_1 = list(
        Battle.objects.filter(player_1_id=user_id, is_over=False)
        .select_related("player_2_id")
        .values(
            "id",
            login=F("player_2_id__login"),
            avatar=F("player_2_id__avatar"),
            sent_id=F("player_2_id"),
        )
    )
    battles_2 = list(
        Battle.objects.filter(player_2_id=user_id, is_over=False)
        .select_related("player_1_id")
        .values(
            "id",
            login=F("player_1_id__login"),
            avatar=F("player_1_id__avatar"),
            sent_id=F("player_1_id"),
        )
    )
    battles = battles_1 + battles_2
    return challenges, my_ended_battles, battles


def other_player(request, obj):
    """возвращает логин другого(не текущего пользователя)
    игрока битвы и айди"""
    user_id = check_and_return_existence_user_id(request)
    if user_id == obj.player_1_id:
        return (
            Battle.objects.filter(
                player_1_id=obj.player_1_id,
                player_2_id=obj.player_2_id,
            )
            .select_related("player_2_id")
            .values_list("player_2_id__login", flat=True)[0]
        ), obj.player_2_id
    else:
        return (
            Battle.objects.filter(
                player_1_id=obj.player_1_id,
                player_2_id=obj.player_2_id,
            )
            .select_related("player_1_id")
            .values_list("player_1_id__login", flat=True)[0]
        ), obj.player_1_id


def other_player_answers(request, obj, round_id):
    other_player_id = other_player(request, obj)[1]
    return len(
        list(
            PlayerAnswer.objects.filter(
                player_id_id=other_player_id,
                round_id_id=round_id
            ).values_list(
                "id",
                flat=True,
            )
        ))


def my_and_opponent_scores(user_id, obj):
    """по айди текущего пользователя и Quesryset Battle
    возвращает очки обоих пользователей"""
    if user_id == obj.player_1_id:
        my_scores = obj.player_1_scores
        other_scores = obj.player_2_scores
    elif user_id == obj.player_2_id:
        my_scores = obj.player_2_scores
        other_scores = obj.player_1_scores
    return my_scores, other_scores


def get_round_now(battle_id):
    """по айди битвы возвращает текущий раунд"""
    return get_object_or_404(
        Battle.objects.only("round_now"), id=battle_id
    ).round_now


def get_chooser(round_now, battle_obj):
    """по текущему раунду и Querysetу Battle с айди игроков
    возвращает кто из них выбирает категорию"""
    if round_now % 2 == 0:
        chooser = battle_obj.player_2_id
    else:
        chooser = battle_obj.player_1_id
    return chooser


def get_rounds_by_battle_id(battle_id):
    """по айди битвы возвращает список всех раундов связанных с ней"""
    rounds = list(
        Round.objects.filter(battle_id_id=battle_id)
        .order_by("id")
        .values(
            "id",
            "is_over",
            "category_id",
        )
    )
    return rounds


def get_answers_in_round(request, rounds, round_now, battle_obj):
    """на вход получает request, rounds(список всех раундов биты),
    round_now(номер какой раунд сейчас 1-6, а не айди раунда!),
    battle_obj(Queryset Battle с айди игроков)"""
    cur_user_answers = []
    other_user_answers = []
    lst_of_round_answers = []
    for round in rounds:
        user_id = check_and_return_existence_user_id(request)
        if round["is_over"]:
            answers = list(
                PlayerAnswer.objects.filter(round_id_id=round["id"]).values(
                    "player_id_id",
                    "is_right",
                    "question_id_id",
                )
            )
            for answer in answers:
                if answer["player_id_id"] == user_id:
                    cur_user_answers.append(
                        (answer["question_id_id"], answer["is_right"], round["id"])
                    )
                else:
                    other_user_answers.append(
                        (answer["question_id_id"], answer["is_right"], round["id"])
                    )
            lst_of_round_answers.append([cur_user_answers, other_user_answers])
            cur_user_answers = []
            other_user_answers = []
        else:
            chooser = get_chooser(round_now, battle_obj)
            answers = list(
                PlayerAnswer.objects.filter(
                    player_id_id=chooser,
                    round_id_id=round["id"],
                ).values_list("question_id_id", "is_right", "round_id_id")
            )
            if len(answers) == 3:
                if user_id == chooser:
                    cur_user_answers += answers
                elif user_id != chooser:
                    other_user_answers += answers
                lst_of_round_answers.append(
                    [
                        cur_user_answers,
                        other_user_answers,
                    ]
                )
            break
    logger.debug(f"{round_now}, раунд сейчас")
    logger.debug(f"{lst_of_round_answers}, ответы игрока")
    return lst_of_round_answers
