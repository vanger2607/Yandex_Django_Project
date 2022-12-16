from django.views.generic import TemplateView


class Battle(TemplateView):
    template_name = "duels/battles.html"
