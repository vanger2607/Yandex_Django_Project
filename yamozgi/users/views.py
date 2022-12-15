from django.shortcuts import redirect, render

from . import forms
from .models import CustomUser


def sign_up(request):
    template_name = 'users/signup.html'
    form = forms.SignupForm(request.POST or None)
    context = {
        'form': form,
    }

    if request.method == 'POST' and form.is_valid():
        login = form.cleaned_data['login']
        mail = form.cleaned_data['email']
        password = form.cleaned_data['password']

        CustomUser.objects.create_user(mail, login, password)
        return redirect('users:signup')

    return render(request, template_name, context)
