import random
import json

from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

from users.models import CustomUser

from questions.models import Question


class Battle(TemplateView):
    template_name = "duels/battles.html"


class UserList(ListView):
    model = CustomUser
    template_name = "test/userlist.html"
    context_object_name = "users"

    def get_queryset(self):
        return (CustomUser.objects.filter(is_active=True)
                                  .only("login", "avatar",))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class QuestionView(TemplateView):
    template_name = "duels/question.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "вопрос"
        ids = Question.objects.values_list("id", flat=True)
        print(ids)
        if ids:
            rand_id = random.choice(ids)
            print(rand_id)
            question = Question.objects.get(pk=rand_id)
            print(question)
        context["question"] = question
        return context


def QuestionAPI(request):
    if request.method == "GET":
        return HttpResponse(status=404)
    elif request.method == "POST":
        data_from_post = json.load(request)
        question_id = data_from_post["question_id"]
        answer = data_from_post["userr_answer"]
        print(answer)
        print(question_id)
        if (
            answer == Question.objects.filter(pk=question_id)
            .only("right_answer")
            .first()
            .right_answer
        ):
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=412)
