from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingrese un correo válido.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Nombre de usuario",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo.")
        return email


class PedirUsuarioForm(forms.Form):
    email = forms.EmailField(
        label="Ingrese el usuario o correo electrónico:",
        widget=forms.EmailInput(attrs={
            'placeholder': 'Usuario o correo electrónico',
            'class': 'form-control'
        })
    )

class PedirContrasenaForm(forms.Form):
    password = forms.CharField(
        label="Ingrese la contraseña:",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control'
        })
    )