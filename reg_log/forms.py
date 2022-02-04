from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from reg_log.models import Client


#Register customer form
class CreateCustomerForm(UserCreationForm):

    class Meta:
        model = User
        fields =  ['first_name', 'username', 'email', 'password1', 'password2']
        exclude = ['user']

#Register Tutor form
class CreateTutorForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        exclude = ['user']
        
class ClientForm(ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ['user', 'email']
