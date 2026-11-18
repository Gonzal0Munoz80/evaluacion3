from django.db import models
import uuid
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class linea(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class producto(models.Model):
    nombre = models.CharField(max_length=100)
    linea = models.ForeignKey(
        linea,
        on_delete=models.CASCADE,
        related_name='productos',
    )
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    porcion = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/',blank=True, null=True)
    apto_celiacos = models.BooleanField(
        default=False,
        verbose_name='Apto para celíacos',
    )
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

        if self.cantidad is not None and self.cantidad < 1:
            errores['cantidad'] = 'La cantidad debe ser al menos 1 unidad.'

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

    