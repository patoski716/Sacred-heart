from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['student_picture', 'level','gender']
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model=Payment
        fields=('user_id','first_name', 'last_name',"amount","email","level","term",)