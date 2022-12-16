from django.views.generic import TemplateView, FormView

from .forms import ProfileForm


class Profile(TemplateView, FormView):
    template_name = "users/profile.html"
    form_class = ProfileForm
