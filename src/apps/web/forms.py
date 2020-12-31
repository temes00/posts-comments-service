import re

from django import forms
from django.forms import PasswordInput


class AuthForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super(AuthForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not password and not username:
            raise forms.ValidationError('You have to write something!')


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    email = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=PasswordInput(), required=True)
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if not password and not email:
            raise forms.ValidationError('You have to write something!')
        if email and not re.match(r'^\S+@\S+\.\S+$', email):
            raise forms.ValidationError('Email field is incorrect!')
