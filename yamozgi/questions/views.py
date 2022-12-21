from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import QuestionForm


class CreateQuestion(CreateView):
    template_name = "questions/creating_question.html"
    form_class = QuestionForm
    success_url = reverse_lazy("questions:create")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
