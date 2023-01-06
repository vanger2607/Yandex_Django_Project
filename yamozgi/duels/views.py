import random
import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404

from users.models import CustomUser
from questions.models import Question
from .models import Challenge, Battle
from .services import context_for_battle_view


class BattleView(TemplateView):
    """страница, на которой отображаются текущие игры,
    брошенные пользователем вызовы
    и вызовы брошенные пользователю"""

    template_name = "duels/battles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Битвы"
        challenges, my_challenges, battles = context_for_battle_view(
            self.request
        )
        context["my_challenges"] = my_challenges
        context["number_of_my_challenges"] = len(my_challenges)
        context["battles"] = battles
        context["number_of_battles"] = len(battles)
        context["challenges"] = challenges
        context["number_of_challenges"] = len(challenges)
        return context


class UserList(ListView):
    model = CustomUser
    template_name = "duels/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        self.queryset = list(
            CustomUser.objects.filter(is_active=True).values(
                "login",
                "avatar",
                "id",
            )
        )
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["number"] = len(self.queryset)
        return context


class QuestionView(TemplateView):
    template_name = "duels/question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "вопрос"
        ids = Question.objects.values_list("id", flat=True)
        if ids:
            rand_id = random.choice(ids)
            question = get_object_or_404(Question, pk=rand_id)
        context["question"] = question
        return context


class DetailBattleView(DetailView):
    pass


def question_api(request):
    if request.method == "GET":
        return HttpResponse(status=404)
    elif request.method == "POST":
        data_from_post = json.load(request)
        question_id = data_from_post["question_id"]
        answer = data_from_post["userr_answer"]
        if (
            answer == Question.objects.filter(pk=question_id)
            .only("right_answer")
            .first()
            .right_answer
        ):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=412)


def challenge_to_other_api(request):
    if request.method == "POST":
        data_from_post = json.load(request)
        from_user_id = data_from_post["from_user"]
        to_user_id = data_from_post["to_user"]
        from_user = get_object_or_404(CustomUser, pk=from_user_id)
        to_user_login = get_object_or_404(CustomUser, pk=to_user_id)
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
        battle_id = obj.pk

        challenge = get_object_or_404(
            Challenge,
            player_recieved_id_id=user_id,
            player_sent_id_id=sent_user_id,
        )
        challenge.delete()
        return JsonResponse({"battle_url": f"battles/{battle_id}"})
