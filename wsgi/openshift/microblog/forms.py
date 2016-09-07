# -*- coding: utf-8 -*-

__author__ = 'Joanna667'
from django.utils import timezone
from django.contrib.auth.models import User
from models import Tag, Article
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(render_value=False))

class ArticleForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    tytul = forms.CharField(max_length=40, min_length=3)
    tresc = forms.CharField(max_length=300, min_length=10, widget=forms.Textarea())

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput())
    email = forms.EmailField(max_length=40, widget=forms.TextInput())
    password1 = forms.CharField(max_length=40, widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=40, widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
          return self.cleaned_data['username']
        raise forms.ValidationError('Użytkownik o takiej nazwie już istnieje!')

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError('Podaj dwa razy to samo haslo')
        return self.cleaned_data