import random
import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView

from users.models import CustomUser
from questions.models import Question
from .models import Challenge


class Battle(TemplateView):
    template_name = "duels/battles.html"


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
        context["number"] = len(self.queryset) // 3
        return context


class QuestionView(TemplateView):
    template_name = "duels/question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "вопрос"
        ids = Question.objects.values_list("id", flat=True)
        if ids:
            rand_id = random.choice(ids)
            question = Question.objects.get(pk=rand_id)
        context["question"] = question
        return context


def QuestionAPI(request):
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


def ChallengeToOtherApi(request):
    if request.method == "POST":
        data_from_post = json.load(request)
        from_user_id = data_from_post["from_user"]
        to_user_id = data_from_post["to_user"]
        from_user = CustomUser.objects.get(pk=from_user_id)
        to_user_login = CustomUser.objects.get(pk=to_user_id)
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
