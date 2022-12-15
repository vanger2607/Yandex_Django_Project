from django.urls import path, re_path

from . import views

app_name = 'users'
urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
]
