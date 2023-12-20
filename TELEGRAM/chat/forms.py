from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from user_app.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="username", widget=forms.TextInput(attrs={'class': 'form-input', 'size': '30', 'rows': '20'}))
    password = forms.CharField(label="password", widget=forms.PasswordInput(attrs={'class': 'form-input', 'size': '30', 'rows': '20'}))


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegistrationForm, self).save(commit=False)
        user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


class ForgetPasswordUser(forms.Form):
    email_reset = forms.EmailField(label="email", widget=forms.TextInput(attrs={'class': 'form-input', 'size': '30', 'rows': '20'}))

class EnterMessageChat(forms.Form):
    enter_chat = forms.CharField(label='enter message in chat', max_length=400, widget=forms.TextInput(attrs={'placeholder':'Enter message'}))