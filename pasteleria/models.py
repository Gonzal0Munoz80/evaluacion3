from django.db import models

# Create your models here.

class producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    porcion = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class encargo(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

    