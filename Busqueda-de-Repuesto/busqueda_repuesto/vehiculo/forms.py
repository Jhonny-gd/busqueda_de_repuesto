from django import forms
from .models import Vehiculo

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['id_auto', 'marca', 'modelo', 'anio', 'transmision', 'tipo']
        widgets = {
            'id_auto': forms.TextInput(attrs={'placeholder': 'Ingrese el ID del vehículo'}),
            'marca': forms.TextInput(attrs={'placeholder': 'Ingrese la marca del vehículo'}),
            'modelo': forms.TextInput(attrs={'placeholder': 'Ingrese el modelo del vehículo'}),
            'anio': forms.NumberInput(attrs={'min': 2000, 'max': 2025, 'placeholder': 'Ingrese el año del vehículo'}),
            'transmision': forms.Select(choices=[
                ('Manual', 'Manual'),
                ('Automática', 'Automática'),
                ('CVT', 'CVT'),
            ]),
            'tipo': forms.Select(choices=[
                ('Suv', 'SUV'),
                ('Pickup', 'Pickup'),
                ('Hatchback', 'Hatchback'),
                ('Coupe', 'Coupé'),
                ('Sedan', 'Sedán'),
                ('Minivan', 'Minivan'),
                ('Híbrido', 'Híbrido'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # 👈 Capturamos el usuario
        super().__init__(*args, **kwargs)

    def clean_id_auto(self):
        id_auto = self.cleaned_data.get('id_auto')
        if Vehiculo.objects.filter(id_auto=id_auto, usuario=self.user).exists():
            raise forms.ValidationError("Ya existe un vehículo con este ID para tu cuenta.")
        return id_auto

    def clean(self):
        cleaned_data = super().clean()
        marca = cleaned_data.get('marca')
        modelo = cleaned_data.get('modelo')
        anio = cleaned_data.get('anio')
        tipo = cleaned_data.get('tipo')
        transmision = cleaned_data.get('transmision')

        if marca and modelo and anio and tipo and transmision:
            if Vehiculo.objects.filter(
                usuario=self.user,
                marca=marca,
                modelo=modelo,
                anio=anio,
                tipo=tipo,
                transmision=transmision
            ).exists():
                raise forms.ValidationError("Ya registraste un vehículo con esta combinación de datos.")
        
        return cleaned_data
