from django.db import models
import uuid
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    porcion = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/',blank=True, null=True)
    visible_en_catalogo = models.BooleanField(default=True, verbose_name='Visible en catálogo')
    def __str__(self):
        return self.nombre

class encargo(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_retiro = models.DateField(null=True, verbose_name='Fecha de retiro')
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    creado = models.DateTimeField(auto_now_add=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2,default=0)
def clean(self):
        super().clean()
        errores = {}

        if self.fecha_retiro and self.fecha_retiro < timezone.localdate():
            errores['fecha_retiro'] = (
                'La fecha de retiro no puede ser anterior a hoy.'
            )

        if self.cantidad is not None and not 1 <= self.cantidad <= 3:
            errores['cantidad'] = 'La cantidad debe estar entre 1 y 3.'

        if (
            self.producto_id
            and self.cantidad is not None
            and self.producto.stock < self.cantidad
        ):
            errores['cantidad'] = 'No hay suficiente stock disponible.'

        if errores:
            raise ValidationError(errores)    

@property
def total(self):
        return self.cantidad * self.precio_unitario
def __str__(self):
        return self.nombre

    