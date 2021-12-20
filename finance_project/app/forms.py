from django.forms import ModelForm
from .models import formInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class dashboardForm(ModelForm):
    class Meta:
        model = formInput
        fields = ('Field', 'Amount')

    widgets = {
        'Field': forms.TextInput(attrs={'class': 'form-control'}),
        'Amount': forms.TextInput(attrs={'class': 'form-control'}),
        # adding new code
        # 'user': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username', 'id': 'elder'}),
    }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
