from django.urls import path

from . import views

app_name = "errors"

urlpatterns = [
    path(
        "smartass_player",
        views.SmartassPlayerError.as_view(),
        name="smartass_error",
    ),
]
