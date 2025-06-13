from pyexpat.errors import messages
from urllib import request
from django import forms
from django.shortcuts import redirect
from .models import Repuesto
from negocio.models import Negocio

class RepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = '__all__'
        widgets = {
            'compatibilidad': forms.SelectMultiple(attrs={
                'id': 'compatibilidad',
                'multiple': 'multiple',
                'style': 'width: 25%; height: 130px;'
                }),
            'foto': forms.ClearableFileInput(attrs={'id': 'imagen', 'style': 'display:none;'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extrae el usuario si se pasó
        super().__init__(*args, **kwargs)
        if user:
            self.fields['negocio'].queryset = Negocio.objects.filter(usuario=user)

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        # Valida máximo 10 dígitos en total y 2 decimales
        if precio >= 10**8:
            raise forms.ValidationError("El precio no puede tener más de 8 dígitos enteros.")
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad > 99999:
            raise forms.ValidationError("La cantidad máxima es 99999.")
        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad

