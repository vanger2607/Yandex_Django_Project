from typing import TypedDict, NamedTuple
import random

from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.db.models import F, QuerySet

from duels.models import (
    Battle,
    Category,
    Challenge,
    CustomUser,
    PlayerAnswer,
    Round,
)
from services.common.common_services import (
    check_and_return_existence_user_id,
)
from yamozgi.settings import LOGGER

# region common functions for duel


def get_chooser(round_now: int, battle_obj: Battle) -> int:
    """по текущему раунду и Querysetу Battle с айди игроков
    возвращает кто из них выбирает категорию."""
    if round_now % 2 == 0:
        return battle_obj.player_2_id
    return battle_obj.player_1_id


def check_correct_user_in_battle_and_return_battle_obj(
    user_id: int, battle_id: int
) -> Battle:
    """проверяет, может ли игрок находится в этой битве
    или пытается попасть в чужую и если все хорошо возвращает battle_obj
    (какой сейчас раунд и айди игроков)."""
    battle_obj = get_object_or_404(
        Battle.objects.only(
            Battle.round_now.field.name,
            Battle.player_1.field.name,
            Battle.player_2.field.name,
            Battle.is_over.field.name,
        ),
        pk=battle_id,
    )
    if not (user_id in [battle_obj.player_2, battle_obj.player_1]):
        raise Http404
    return battle_obj


class BaseBattleDict(TypedDict):
    id: int
    login: str
    avatar: str


class EndedBattleDict(BaseBattleDict):
    recieved_id: int


class CurrentBattleDict(BaseBattleDict):
    sent_id: int


class CurrentbattlesChallengesEndedbattles(NamedTuple):
    challenges: list[dict[str, int]]
    my_ended_battles: list[EndedBattleDict]
    battles: list[CurrentBattleDict]


def _get_ended_battles(user_id: int) -> list[EndedBattleDict]:
    """получаю списки  законченных битв пользователя +
    + никнеймы и аватары пользователей, которые закончили эту битву."""
    my_ended_battles_1 = list(
        Battle.objects.filter(player_1_id=user_id, is_over=True)
        .select_related("player_2_id")
        .values(
            Battle.id.field.name,
            login=F(
                f"{Battle.player_1.field.name}__{CustomUser.login.field.name}"
            ),
            avatar=F(
                f"{Battle.player_1.field.name}__{CustomUser.avatar.field.name}"
            ),
            recieved_id=F(Battle.player_2.field.name),
        )
    )
    my_ended_battles_2 = list(
        Battle.objects.filter(player_2_id=user_id, is_over=True)
        .select_related(Battle.player_1.field.name)
        .values(
            Battle.id.field.name,
            login=F("player_1_id__login"),
            avatar=F("player_1_id__avatar"),
            recieved_id=F("player_1_id"),
        )
    )
    return my_ended_battles_1 + my_ended_battles_2


def _get_current_battle(user_id: int) -> list[CurrentBattleDict]:
    """получаю списки текущих игр + никнеймы и аватары пользователей,
    против которых идет игра(сначала получаю список игр,
    где id текущего пользователя равен player_1_id,
    потом player_2_id, после складываю эти списки
    в переменную battles)."""
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
    return battles_1 + battles_2


# endregion

# region functions for BattleView


def context_for_battle_view(
    request: HttpRequest,
) -> CurrentbattlesChallengesEndedbattles:
    """функция на вход получает request,
    делает запросы к бд и возвращает список вызовов (challenges),
    брошенных текущему пользователю,
    список сыгранных битв (ended_battles),
    список текущих игр (battles)."""

    user_id = check_and_return_existence_user_id(request)

    challenges = list(
        Challenge.objects.filter(player_recieved_id=request.user)
        .select_related("player_sent_id")
        .values(
            login=F("player_sent_id__login"),
            avatar=F("player_sent_id__avatar"),
            sent_id=F("player_sent_id"),
        )
    )

    my_ended_battles = _get_ended_battles(user_id)
    battles = _get_current_battle(user_id)
    return CurrentbattlesChallengesEndedbattles(
        challenges,
        my_ended_battles,
        battles,
    )


# endregion

# region functions for DetailBattleView


class RoundMetaDict(TypedDict):
    id: int
    is_over: bool
    category_id: int


def get_rounds_by_battle_id(battle_id: int) -> list[RoundMetaDict]:
    """по айди битвы возвращает список всех раундов связанных с ней."""
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


def check_correct_user_in_battle_by_obj_and_return_battle_obj(
    user_id: int, battle_obj: Battle
) -> Battle:
    """проверяет, может ли игрок находится в этой битве
    или пытается попасть в чужую и если все хорошо возвращает battle_obj
    (какой сейчас раунд и айди игроков)."""
    if user_id not in (battle_obj.player_2_id, battle_obj.player_1_id):
        raise Http404
    return battle_obj


class AnswersInRound(NamedTuple):
    question_id: int
    is_right: bool
    round_id: int


def get_answers_in_round(
    request: HttpRequest,
    rounds: list[RoundMetaDict],
    round_now: int,
    battle_obj: Battle,
) -> list[list[list[AnswersInRound]]]:
    """на вход получает request, rounds(список всех раундов биты),
    round_now(номер какой раунд сейчас 1-6, а не айди раунда!),
    battle_obj(Queryset Battle с айди игроков)."""
    cur_user_answers = []
    other_user_answers = []
    lst_of_round_answers = []
    for nth_round in rounds:
        user_id = check_and_return_existence_user_id(request)
        if nth_round["is_over"]:
            answers = list(
                PlayerAnswer.objects.filter(
                    round_id_id=nth_round["id"]
                ).values(
                    "player_id_id",
                    "is_right",
                    "question_id_id",
                )
            )
            for answer in answers:
                if answer["player_id_id"] == user_id:
                    cur_user_answers.append(
                        (
                            answer["question_id_id"],
                            answer["is_right"],
                            nth_round["id"],
                        )
                    )
                else:
                    other_user_answers.append(
                        (
                            answer["question_id_id"],
                            answer["is_right"],
                            nth_round["id"],
                        )
                    )
            lst_of_round_answers.append([cur_user_answers, other_user_answers])
            cur_user_answers = []
            other_user_answers = []
        else:
            chooser = get_chooser(round_now, battle_obj)
            answers = list(
                PlayerAnswer.objects.filter(
                    player_id_id=chooser,
                    round_id_id=nth_round["id"],
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
    return lst_of_round_answers


Current_user_scores = int
Opponent_scores = int


def my_and_opponent_scores(
    user_id: int, obj: Battle
) -> tuple[Current_user_scores, Opponent_scores]:
    """по айди текущего пользователя и Quesryset Battle
    возвращает очки обоих пользователей."""
    if user_id == obj.player_1_id:
        my_scores = obj.player_1_scores
        other_scores = obj.player_2_scores
    elif user_id == obj.player_2_id:
        my_scores = obj.player_2_scores
        other_scores = obj.player_1_scores
    return my_scores, other_scores


# endregion

# region functions for RoundChooseView


def is_len_player_answers_equal_three(user_id: int, round_id: int) -> bool:
    """навход принимает айди игрока и айди раунда,
    проверяет равно ли кол-во ответов игрока в раунде трем,
    если это так - возвращает True, иначе False."""
    len_answers = len(
        list(
            PlayerAnswer.objects.filter(
                player_id_id=user_id,
                round_id_id=round_id,
            ).values_list(
                "id",
                flat=True,
            )
        )
    )
    return len_answers == 3


class Dct_with_params_for_redirect(TypedDict):
    pk: int
    round: int
    pos: int
    user_id: int


class Parametrs_for_redirect(NamedTuple):
    url: str
    dct_with_parametrs: Dct_with_params_for_redirect


def handler_for_category_in_round_and_player_is_chooser(
    user_id: int, browse_params: dict[str, int]
) -> Parametrs_for_redirect:
    """проверяет ответил ли пользователь на все три вопроса в раунде -
    - возвращает параметры для redirect"""
    if is_len_player_answers_equal_three(user_id, browse_params["round"]):
        return (
            Parametrs_for_redirect(
                "duels:question-complete",
                Dct_with_params_for_redirect(
                    pk=browse_params["pk"],
                    round=browse_params["round"],
                    pos=1,
                    user_id=user_id,
                ),
            ),
            True,
        )
    else:
        return Parametrs_for_redirect(
            "duels:question",
            Dct_with_params_for_redirect(
                pk=browse_params["pk"],
                round=browse_params["round"],
                pos=1,
            ),
        )


def handler_for_category_in_round_and_player_is_not_chooser(
    user_id: int, browse_params: dict[str, int]
) -> Parametrs_for_redirect:
    """проверяет ответил ли пользователь на все три вопроса в раунде -
    - возвращает параметры для redirect"""
    if is_len_player_answers_equal_three(user_id, browse_params["round"]):
        return Parametrs_for_redirect(
            "duels:question",
            Dct_with_params_for_redirect(
                pk=browse_params["pk"],
                round=browse_params["round"],
                pos=1,
            ),
        )

    return False, False, False


class GeneratedCategories(NamedTuple):
    first_category: QuerySet[Category]
    second_category: QuerySet[Category]
    third_category: QuerySet[Category]


def generate_categories() -> GeneratedCategories:
    """создает три категории и возвращает их"""
    ids = list(Category.objects.values_list("id", flat=True))
    if ids:
        random.shuffle(ids)
        first_category = get_object_or_404(Category, pk=ids[0])
        second_category = get_object_or_404(Category, pk=ids[1])
        third_category = get_object_or_404(Category, pk=ids[2])
        return GeneratedCategories(
            first_category,
            second_category,
            third_category,
        )
    LOGGER.error("елы-палы не смогли получить айди категорий!")
    raise 404


# endregion
