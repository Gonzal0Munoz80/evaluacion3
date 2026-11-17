from django import forms

from .models import encargo


class EncargoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        min_value=1,
        max_value=3,
        initial=1,
        label='Cantidad de unidades',
    )

    class Meta:
        model = encargo
        fields = ('nombre', 'correo', 'telefono', 'fecha_retiro', 'cantidad')
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
