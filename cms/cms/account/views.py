from django.shortcuts import render
from django.views.generic import CreateView
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import  UserCreationForm
from account.forms import SignUpForm
from django.urls import reverse_lazy
from django.conf import settings
# Create your views here.

class SignUpView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")