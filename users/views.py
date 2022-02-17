from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from .forms import RegisterForm
# Create your views here.

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = '/'


class UserLoginView(LoginView):

    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    template_name = 'users/login.html'

