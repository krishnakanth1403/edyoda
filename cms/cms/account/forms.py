from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.conf import settings
from django import forms
from account.models import User

class SignUpForm(UserCreationForm):
    
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')