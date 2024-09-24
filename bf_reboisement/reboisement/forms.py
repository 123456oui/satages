from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',  # ou "Nom d'utilisateur" selon ton besoin
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'id': 'id_username'  # ID pour lier avec le label
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'id': 'id_password'  # ID pour lier avec le label et pour le JS
        })
    )
