from django.db import models
import uuid
# Create your models here.

class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    porcion = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='productos/',blank=True, null=True)
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
    @property
    def total(self):
        return self.cantidad * self.precio_unitario
    def __str__(self):
        return self.nombre

    