from django.views.generic import TemplateView, ListView

from users.models import CustomUser


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
