from django.contrib import admin
from .models import producto, encargo
# Register your models here.
@admin.register(producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'stock', 'porcion')
    search_fields = ('nombre', 'descripcion')


@admin.register(encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'producto')
    search_fields = ('nombre', 'correo', 'telefono', 'producto__nombre')
