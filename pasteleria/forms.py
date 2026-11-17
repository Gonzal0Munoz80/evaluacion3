from django import forms

from .models import encargo


class EncargoForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        initial=1,
        label='Cantidad de unidades',
    )

    def __init__(self, *args, producto=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.producto = producto

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']

        if cantidad < 1:
            raise forms.ValidationError(
                'La cantidad debe ser al menos 1 unidad.'
            )
        if self.producto and cantidad > self.producto.stock:
            raise forms.ValidationError(
                f'Solo hay {self.producto.stock} unidades disponibles.'
            )
        return cantidad

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
