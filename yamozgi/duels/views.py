import random
import json
import datetime
from typing import Any


from django.http import HttpRequest, HttpResponse
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from users.models import CustomUser
from questions.models import Question

from .models import Challenge, Battle, Round, PlayerAnswer

from services.common.common_services import (
    check_and_return_existence_user_id,
    other_player,
)
from services.duels.views_services import (
    get_rounds_by_battle_id,
    check_correct_user_in_battle_by_obj_and_return_battle_obj,
    check_correct_user_in_battle_and_return_battle_obj,
    context_for_battle_view,
    get_answers_in_round,
    get_chooser,
    my_and_opponent_scores,
    generate_categories,
    handler_for_category_in_round_and_player_is_chooser,
    handler_for_category_in_round_and_player_is_not_chooser,
    can_see_answers,
    check_correct_user_obj_in_battle_and_return_battle_obj,
)
from yamozgi.settings import BASE_URL, LOGGER


class BattleView(LoginRequiredMixin, TemplateView):
    """страница, на которой отображаются текущие игры,
    брошенные пользователем вызовы
    и вызовы брошенные пользователю"""

    login = reverse_lazy("users:signin")
    template_name = "duels/battles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenges, my_ended_battles, battles = context_for_battle_view(
            self.request
        )
        context["my_ended_battles"] = my_ended_battles
        context["number_of_my_ended_battles"] = len(my_ended_battles)
        context["battles"] = battles
        context["number_of_battles"] = len(battles)
        context["challenges"] = challenges
        context["number_of_challenges"] = len(challenges)
        context["base_url"] = BASE_URL
        context["title"] = "Битвы"
        return context


class UserList(ListView):
    """страница отображающая всех юзеров, которым можно кинуть вызов"""

    model = CustomUser
    template_name = "duels/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        self.queryset = list(
            CustomUser.objects.filter(is_active=True).values(
                CustomUser.login.field.name,
                CustomUser.avatar.field.name,
                CustomUser.id.field.name,
            )
        )
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["number"] = len(self.queryset)
        context["base_url"] = BASE_URL
        return context


class QuestionView(TemplateView):
    template_name = "duels/question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ids = None
        user = self.request.user
        check_correct_user_obj_in_battle_and_return_battle_obj(
            user,
            self.kwargs["pk"],
        )
        round_questions = get_object_or_404(
            Round.objects.only(
                "category_id", "id", "question_1", "question_2", "question_3"
            ),
            id=self.kwargs["round"],
        )
        if self.kwargs["pos"] == 1 and not round_questions.question_1:
            ids = Question.objects.filter(
                category_id=round_questions.category_id, is_approved=True
            ).values_list("id", flat=True)
            if ids:
                rand_id = random.choice(ids)
                question = get_object_or_404(Question, pk=rand_id)
                round_questions.question_1 = question
                round_questions.save()
        elif self.kwargs["pos"] == 1 and round_questions.question_1:
            question = round_questions.question_1
        elif self.kwargs["pos"] == 2 and not round_questions.question_1:
            raise Http404
        elif self.kwargs["pos"] == 2 and not round_questions.question_2:
            ids = list(
                Question.objects.filter(
                    category_id=round_questions.category_id, is_approved=True
                ).values_list("id", flat=True)
            )
            ids.remove(round_questions.question_1_id)
            if ids:
                rand_id = random.choice(ids)
                question = get_object_or_404(Question, pk=rand_id)
                round_questions.question_2 = question
                round_questions.save()
        elif self.kwargs["pos"] == 2 and round_questions.question_2:
            question = round_questions.question_2
        elif self.kwargs["pos"] == 3 and not round_questions.question_2:
            raise Http404
        elif self.kwargs["pos"] == 3 and not round_questions.question_3:
            ids = list(
                Question.objects.filter(
                    category_id=round_questions.category_id, is_approved=True
                ).values_list("id", flat=True)
            )
            ids.remove(round_questions.question_1_id)
            ids.remove(round_questions.question_2_id)
            if ids:
                rand_id = random.choice(ids)
                question = get_object_or_404(Question, pk=rand_id)
                round_questions.question_3 = question
                round_questions.save()
        elif self.kwargs["pos"] == 3 and round_questions.question_3:
            question = round_questions.question_3
        context["question"] = question
        context["question_now"] = self.kwargs["pos"]
        context["round_id"] = self.kwargs["round"]
        context["title"] = "вопрос"
        context["battle_now"] = self.kwargs["pk"]
        context["base_url"] = BASE_URL
        context["round_now"] = (
            len(
                Round.objects.filter(
                    battle_id_id=self.kwargs["pk"], is_over=True
                ).values_list(
                    "id",
                    flat=True,
                )
            )
            + 1
        )
        return context


class QuestionCompleteView(TemplateView):
    template_name = "duels/question-complete.html"
    # внизу костыль, чтобы пременные можно было видеть и в dispatch и в context
    user_id = None
    current_user_id = None
    can_see = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        self.user_id = self.kwargs["user_id"]
        self.current_user_id = check_and_return_existence_user_id(self.request)
        LOGGER.debug(self.request.user.id)
        check_correct_user_in_battle_and_return_battle_obj(
            self.current_user_id,
            self.kwargs["pk"],
        )
        LOGGER.debug(self.kwargs["round"])
        LOGGER.debug(self.user_id)
        self.can_see = can_see_answers(
            self.current_user_id,
            self.kwargs["round"],
            self.user_id,
        )
        if not (self.can_see):
            return redirect("errors:smartass_error")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.can_see:
            len_answers = len(
                list(
                    PlayerAnswer.objects.filter(
                        player_id_id=self.user_id,
                        round_id_id=self.kwargs["round"],
                    ).values_list(
                        "id",
                        flat=True,
                    )
                )
            )
            if len_answers == 3 and self.kwargs["pos"] != 3:
                context["next_question"] = True
                context["next_question_url"] = (
                    f"{BASE_URL}/battles/{self.kwargs['pk']}"
                    f"/rounds/{self.kwargs['round']}"
                    f"/question_pos/{self.kwargs['pos'] + 1}"
                    f"/complete/user/{self.user_id}"
                )
            elif self.kwargs["pos"] == 3:
                context["next_question"] = False
                context["next_question_url"] = (
                    f"{BASE_URL}/battles/" f"{self.kwargs['pk']}"
                )
            elif len_answers != 3:
                context["next_question"] = True
                context["next_question_url"] = (
                    f"{BASE_URL}/battles/{self.kwargs['pk']}"
                    f"/rounds/{self.kwargs['round']}"
                    f"/question_pos/{self.kwargs['pos'] + 1}"
                )
            question_id = get_object_or_404(
                Round.objects.values_list(
                    f"question_{self.kwargs['pos']}_id",
                    flat=True,
                ),
                id=self.kwargs["round"],
            )
            question = get_object_or_404(Question, pk=question_id)
            player_answer = get_object_or_404(
                PlayerAnswer,
                player_id_id=self.user_id,
                round_id_id=self.kwargs["round"],
                question_id_id=question_id,
            )
            context["question"] = question
            context["question_now"] = self.kwargs["pos"]
            context["player_answer"] = player_answer.player_answer
            return context


class RoundChooseView(TemplateView):
    """вьюха выбора категории для раунда"""

    template_name = "duels/choose_category.html"
    to_redirect = False
    redirect_data = ""

    def post(self, request, *args, **kwargs):
        category = self.request.POST.get("category", None)
        round = get_object_or_404(Round, pk=self.kwargs["round"])
        round.category_id = category
        round.save()
        return redirect(
            "duels:question",
            pk=self.kwargs["pk"],
            round=self.kwargs["round"],
            pos=1,
        )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.to_redirect:
            return self.redirect_data
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_now = (
            len(
                Round.objects.filter(
                    battle_id_id=self.kwargs["pk"], is_over=True
                ).values_list(
                    "id",
                    flat=True,
                )
            )
            + 1
        )
        user_id = check_and_return_existence_user_id(self.request)
        category = get_object_or_404(
            Round.objects.only("category_id"), pk=self.kwargs["round"]
        )
        battle_obj = check_correct_user_in_battle_and_return_battle_obj(
            user_id,
            self.kwargs["pk"],
        )
        round = get_object_or_404(
            Round.objects.only(
                "question_1_id",
                "question_2_id",
                "question_3_id",
                "is_over",
            ),
            pk=self.kwargs["round"],
        )
        chooser = get_chooser(round_now, battle_obj)
        LOGGER.debug(f"choose round {round_now}")
        if not category.category_id:
            if user_id == chooser:
                (
                    first_category,
                    second_category,
                    third_category,
                ) = generate_categories()
                context["first_category"] = first_category
                context["second_category"] = second_category
                context["third_category"] = third_category
                context["chooser"] = True
            else:
                context["chooser"] = False
        elif category.category_id and user_id == chooser and not round.is_over:
            self.to_redirect = True

            url, params = handler_for_category_in_round_and_player_is_chooser(
                user_id,
                self.kwargs,
            )
            self.redirect_data = redirect(url, **params)
        elif category.category_id and user_id != chooser and not round.is_over:
            (
                url,
                params,
            ) = handler_for_category_in_round_and_player_is_not_chooser()
            if url:
                self.to_redirect = True
                self.redirect_data(url, **params)
        elif category.category_id and round.is_over:
            LOGGER.debug("мы в конце раунда все хорошо")
            self.redirect_data = redirect(
                "duels:question-complete",
                pk=self.kwargs["pk"],
                round=self.kwargs["round"],
                pos=1,
                user_id=user_id,
            )
        context["battle_id"] = self.kwargs["pk"]
        return context


class DetailBattleView(DetailView):
    model = Battle
    template_name = "duels/battle.html"
    context_object_name = "battle"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = check_and_return_existence_user_id(self.request)
        battle = check_correct_user_in_battle_by_obj_and_return_battle_obj(
            user_id,
            self.object,
        )
        user_name, other_user_id = other_player(self.request, self.object)
        my_scores, opponent_scores = my_and_opponent_scores(
            user_id, self.object
        )
        round = battle.round_now
        round_now = (
            len(
                Round.objects.filter(
                    battle_id_id=self.kwargs["pk"], is_over=True
                ).values_list(
                    "id",
                    flat=True,
                )
            )
            + 1
        )
        LOGGER.debug(f"{round_now}, раунд тута")
        round_category = get_object_or_404(
            Round.objects.values_list("category_id__name", flat=True), pk=round
        )
        rounds = get_rounds_by_battle_id(battle.pk)
        answers = get_answers_in_round(self.request, rounds, round_now, battle)
        context["title"] = f"Игра с {user_name}"
        context["other_player"] = user_name
        context["right"] = True
        context["rounds"] = rounds
        context["answers"] = answers
        context["base_url"] = BASE_URL
        context["battle_id"] = self.kwargs["pk"]
        context["other_user_id"] = other_user_id
        context["user_id"] = user_id
        context["round_now"] = round_now
        context["round_url"] = (
            f"{BASE_URL}/battles/" f"{self.kwargs['pk']}/rounds/{round}"
        )
        context["my_scores"] = my_scores
        context["opponent_scores"] = opponent_scores
        context["has_ended"] = self.object.is_over
        context["category_name"] = round_category
        return context


def question_api_start(request):
    user_id = check_and_return_existence_user_id(request)
    data_from_post = json.load(request)
    question_id = data_from_post["question_id"]
    round_id = data_from_post["round_id"]
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        PlayerAnswer.objects.get(
            player_id_id=user_id,
            round_id_id=round_id,
            question_id_id=question_id,
        )
    except PlayerAnswer.DoesNotExist:
        PlayerAnswer.objects.create(
            player_id_id=user_id,
            round_id_id=round_id,
            question_id_id=question_id,
            start_answering=time_now,
        )

    return HttpResponse(status=200)


def question_api_endtime(request):
    user_id = check_and_return_existence_user_id(request)
    if request.method == "GET":
        return HttpResponse(status=404)
    elif request.method == "POST":
        data_from_post = json.load(request)
        question_id = data_from_post["question_id"]
        battle = get_object_or_404(Battle, pk=data_from_post["battle_now"])
        player_answer = get_object_or_404(
            PlayerAnswer,
            player_id_id=user_id,
            round_id_id=data_from_post["round_id"],
            question_id_id=question_id,
        )
        if not player_answer.player_answer:
            player_answer.is_right = False
            player_answer.player_answer = "timeout"
            player_answer.save()
        if int(data_from_post["question_now"]) == 3:
            oth_player_id = other_player(request, battle)[1]
            len_answers = len(
                list(
                    PlayerAnswer.objects.filter(
                        player_id_id=oth_player_id,
                        round_id_id=data_from_post["round_id"],
                    ).values_list(
                        "id",
                        flat=True,
                    )
                )
            )
            if len_answers == 3 and data_from_post["round_now"] != 6:
                round = get_object_or_404(Round, pk=data_from_post["round_id"])
                round.is_over = True
                round.save()
                next_round = Round.objects.filter(
                    battle_id_id=data_from_post["battle_now"], is_over=False
                ).first()
                battle.round_now = next_round.pk
                battle.save()
            elif (
                len_answers == 3
                and data_from_post["round_now"] == 6
                and int(data_from_post["question_now"]) == 3
            ):
                round = get_object_or_404(Round, pk=data_from_post["round_id"])
                round.is_over = True
                round.save()
                battle.is_over = True
                battle.save()
    return JsonResponse(
        {
            "question_url": (
                f"{BASE_URL}/battles/"
                f"{data_from_post['battle_now']}"
                f"/rounds/{data_from_post['round_id']}"
                f"/question_pos/{data_from_post['question_now']}/"
                f"complete/user/{user_id}"
            )
        }
    )


def question_api(request):
    user_id = check_and_return_existence_user_id(request)
    if request.method == "GET":
        return HttpResponse(status=404)
    elif request.method == "POST":
        LOGGER.debug("question api start")
        time_now = datetime.datetime.strptime(
            f'{datetime.datetime.now().strftime("%H:%M:%S")}', "%H:%M:%S"
        )
        data_from_post = json.load(request)
        question_id = data_from_post["question_id"]
        answer = data_from_post["userr_answer"]
        question = get_object_or_404(Question, pk=question_id)
        right = False
        player_answer = get_object_or_404(
            PlayerAnswer,
            player_id_id=user_id,
            round_id_id=data_from_post["round_id"],
            question_id_id=question_id,
        )
        battle = get_object_or_404(Battle, pk=data_from_post["battle_now"])
        in_time = False
        try:
            timer = time_now - datetime.datetime.strptime(
                player_answer.start_answering.strftime("%H:%M:%S"),
                "%H:%M:%S",
            )
            if int(timer.total_seconds()) <= 24:
                in_time = True
        except Exception:
            raise Http404
        LOGGER.debug(
            f"question api таймер , {timer.total_seconds()}, {in_time}"
        )
        if answer == question.right_answer and in_time:
            LOGGER.debug("question api вошли в правильный ответ")
            right = True
            if user_id == battle.player_1_id:
                battle.player_1_scores += 1
            elif user_id == battle.player_2_id:
                battle.player_2_scores += 1
            battle.save()

        if not in_time:
            answer = "timeout"
        if not player_answer.player_answer:
            LOGGER.debug("question api вошли в сохранения ответа пользователя")
            player_answer.is_right = right
            player_answer.player_answer = answer
            player_answer.save()
        if int(data_from_post["question_now"]) == 3:
            LOGGER.debug("question api если третий вопрос")
            oth_player_id = other_player(request, battle)[1]
            len_answers = len(
                list(
                    PlayerAnswer.objects.filter(
                        player_id_id=oth_player_id,
                        round_id_id=data_from_post["round_id"],
                    ).values_list(
                        "id",
                        flat=True,
                    )
                )
            )
            LOGGER.debug(
                f"question api длина ответов другого игрока, {len_answers}"
            )
            if len_answers == 3 and data_from_post["round_now"] != 6:
                LOGGER.debug("question api вошли в завершение раунда")
                round = get_object_or_404(Round, pk=data_from_post["round_id"])
                round.is_over = True
                round.save()
                next_round = Round.objects.filter(
                    battle_id_id=data_from_post["battle_now"], is_over=False
                ).first()
                battle.round_now = next_round.pk
                battle.save()
                LOGGER.debug("question api все прошло успешно")
            elif (
                len_answers == 3
                and data_from_post["round_now"] == 6
                and int(data_from_post["question_now"]) == 3
            ):
                round = get_object_or_404(Round, pk=data_from_post["round_id"])
                round.is_over = True
                round.save()
                battle.is_over = True
                battle.save()
        return JsonResponse(
            {
                "question_url": (
                    f"{BASE_URL}/battles/"
                    f"{data_from_post['battle_now']}"
                    f"/rounds/{data_from_post['round_id']}"
                    f"/question_pos/{data_from_post['question_now']}/"
                    f"complete/user/{user_id}"
                )
            }
        )


def challenge_to_other_api(request):
    if request.method == "POST":
        data_from_post = json.load(request)
        from_user_id = data_from_post["from_user"]
        to_user_id = data_from_post["to_user"]
        from_user = get_object_or_404(CustomUser, pk=from_user_id)
        to_user_login = get_object_or_404(CustomUser, pk=to_user_id)
        is_battle_sent_by_me_exist = Battle.objects.filter(
            player_1=from_user_id, player_2=to_user_id
        ).exists()
        is_battle_sent_to_me_exist = Battle.objects.filter(
            player_1=to_user_id, player_2=from_user_id
        ).exists()
        if is_battle_sent_by_me_exist and is_battle_sent_to_me_exist:
            return JsonResponse(
                {
                    "messages": (
                        "У Вас уже и так две битвы"
                        "с этим игроком, куда уж больше?!"
                    ),
                    "error": True,
                }
            )
        challenge, created = Challenge.objects.get_or_create(
            player_sent_id=from_user, player_recieved_id=to_user_login
        )
        if not created and challenge:
            return JsonResponse(
                {
                    "messages": f"Вы уже бросили вызов {to_user_login}"
                    f" дождитесь когда он/а его примет"
                }
            )
    return JsonResponse({"messages": f"{to_user_login} получил/а Ваш вызов"})


def decline_challenge_api(request):
    if request.method == "POST":
        data_from_post = json.load(request)
        if request.user and request.user.id:
            user_id = request.user.id
        else:
            raise Http404
        sent_user_id = data_from_post["sent_user_id"]
        challenge = get_object_or_404(
            Challenge,
            player_recieved_id_id=user_id,
            player_sent_id_id=sent_user_id,
        )
        challenge.delete()
        return HttpResponse(status=200)


def decline_my_challenge_api(request):
    if request.method == "POST":
        data_from_post = json.load(request)
        if request.user and request.user.id:
            user_id = request.user.id
        else:
            raise Http404
        recieved_user_id = data_from_post["recieved_user_id"]
        challenge = get_object_or_404(
            Challenge,
            player_recieved_id_id=recieved_user_id,
            player_sent_id_id=user_id,
        )
        challenge.delete()
        return HttpResponse(status=200)


def accept_challenge_api(request):
    if request.method == "POST":
        data_from_post = json.load(request)
        if request.user and request.user.id:
            user_id = request.user.id
        else:
            raise Http404
        sent_user_id = data_from_post["sent_user_id"]
        obj, created = Battle.objects.get_or_create(
            player_1_id=user_id,
            player_2_id=sent_user_id,
            is_over=False,
        )
        print("obj")
        battle_id = obj.pk
        if created:
            Round.objects.bulk_create(
                [
                    Round(battle_id_id=battle_id, is_over=False),
                    Round(battle_id_id=battle_id, is_over=False),
                    Round(battle_id_id=battle_id, is_over=False),
                    Round(battle_id_id=battle_id, is_over=False),
                    Round(battle_id_id=battle_id, is_over=False),
                    Round(battle_id_id=battle_id, is_over=False),
                ]
            )
        next_round = Round.objects.filter(
            battle_id_id=battle_id, is_over=False
        ).first()
        obj.round_now = next_round.pk
        obj.save()
        print("saved obj")
        challenge = get_object_or_404(
            Challenge,
            player_recieved_id_id=user_id,
            player_sent_id_id=sent_user_id,
        )
        challenge.delete()
        print("all_good", obj)
        return JsonResponse({"battle_url": f"battles/{battle_id}"})
