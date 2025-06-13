import re
from django import forms
from .models import Cotizante, VehiculoCotizacion, DetalleRepuestoCotizado
from vehiculo.models import Vehiculo

class CotizanteForm(forms.ModelForm):
    class Meta:
        model = Cotizante
        vehiculos = Vehiculo.objects.all()
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'dui']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre completo'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'telefono': forms.TextInput(attrs={
                'pattern': r'^\d{8}$',
                'title': 'Debe tener exactamente 8 dígitos',
                'maxlength': 8,
                'inputmode': 'numeric',
                'placeholder': 'Teléfono'}),
            'dui': forms.TextInput(attrs={
                'pattern': r'^\d{8}-\d$',
                'title': 'Debe tener formato: 12345678-9',
                
                'maxlength': 10,
                'placeholder': '12345678-9'}),
        }
        def clean_dui(self):
             dui = self.cleaned_data.get('dui')
             if not re.match(r'^\d{8}-\d$', dui):
                  raise forms.ValidationError("Formato de DUI inválido. Ej: 12345678-9")
                  return dui

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{8}$', telefono):
            raise forms.ValidationError("Teléfono debe tener exactamente 8 dígitos")
        return telefono


class VehiculoCotizacionForm(forms.ModelForm):
    class Meta:
        model = VehiculoCotizacion
        fields = ['marca', 'modelo', 'anio', 'transmision', 'tipo']
        widgets = {
            'marca': forms.TextInput(attrs={'placeholder': 'Marca del vehículo'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Modelo'}),
            'anio': forms.NumberInput(attrs={'placeholder': 'Año'}),
            'transmision': forms.TextInput(attrs={'placeholder': 'Transmisión'}),
            'tipo': forms.TextInput(attrs={'placeholder': 'Tipo de vehículo'}),
            
        }


class DetalleRepuestoCotizadoForm(forms.ModelForm):
    class Meta:
        model = DetalleRepuestoCotizado
        fields = ['repuesto', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'min': 1}),
        }