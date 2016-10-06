# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class AdminUserCreationForm(forms.ModelForm):

    email = forms.EmailField(label='Correo electrónico')
    
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmación de la contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

    def save(self, commit=True):
        user = super(AdminUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



class AdminUserChangeForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField(label='Contraseña')

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']
