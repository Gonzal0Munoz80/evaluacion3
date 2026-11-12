from django import forms

from .models import encargo


class EncargoForm(forms.ModelForm):
    class Meta:
        model = encargo
        fields = ('nombre', 'correo', 'telefono', 'fecha_retiro')
        labels = {
            'nombre': 'Tu nombre',
            'correo': 'Correo electrónico',
            'telefono': 'Teléfono',
            'fecha_retiro': 'Fecha de retiro',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'autocomplete': 'name'}),
            'correo': forms.EmailInput(attrs={'autocomplete': 'email'}),
            'telefono': forms.TextInput(
                attrs={'type': 'tel', 'autocomplete': 'tel'}
            ),
            'fecha_retiro': forms.DateInput(attrs={'type': 'date'}),
        }
