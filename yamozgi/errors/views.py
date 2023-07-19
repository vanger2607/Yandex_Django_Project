from typing import Any, Dict
from django.views.generic import TemplateView


class SmartassPlayerError(TemplateView):
    template_name = "errors\\smartass_player_error.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        came_from = self.request.META.get('HTTP_REFERER')
        context = super().get_context_data(**kwargs)
        context['title'] = 'Уведомление о наглости'
        context['came_from'] = came_from
        return context
