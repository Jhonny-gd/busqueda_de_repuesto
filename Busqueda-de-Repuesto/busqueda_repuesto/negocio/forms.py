from django import forms
from .models import Negocio

class NegocioForm(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = ['codigo', 'nombre', 'nit', 'ubicacion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT'}),
            'ubicacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ubicación'}),
        }