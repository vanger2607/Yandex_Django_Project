from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import QuestionForm
from .models import Question
from .models import Question


class CreateQuestion(LoginRequiredMixin, FormView):
    template_name = "questions/creating_question.html"
    form_class = QuestionForm

    def form_valid(self, form):
        self.success_url = reverse_lazy("questions:create-question")
        question = Question.objects.create(
            question_text=form.cleaned_data["question_text"],
            question_choice1=form.cleaned_data["question_choice1"],
            question_choice2=form.cleaned_data["question_choice2"],
            question_choice3=form.cleaned_data["question_choice3"],
            question_choice4=form.cleaned_data["question_choice4"],
            right_answer=form.cleaned_data["right_answer"],
            category=form.cleaned_data["category"],
            author_id=self.request.user.pk
        )

        question.save()
        messages.success(
            self.request,
            ("Вопрос был отправлен на проверку"),
            extra_tags="alert",
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
