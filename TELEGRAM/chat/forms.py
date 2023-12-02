from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm

from user_app.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'class': 'form-input', 'size': '30', 'rows': '20'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'form-input', 'size': '30', 'rows': '20'}))


class RegistrationForm(UserCreationForm, ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ForgetPasswordUser(forms.Form):
    email_reset = forms.EmailField(label="email", widget=forms.TextInput(attrs={'class': 'form-input', 'size': '30', 'rows': '20'}))