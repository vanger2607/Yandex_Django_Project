from django.urls import path

from . import views

app_name = "duels"

urlpatterns = [
    path(
        "battles",
        views.Battle.as_view(),
        name="battles",
    ),
]
