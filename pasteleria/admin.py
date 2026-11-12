from django.contrib import admin
from django.utils.html import format_html

from .models import producto, encargo


# Register your models here.
@admin.register(producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
        'precio_formateado',
        'stock',
        'porcion',
        'imagen_preview',
    )
    readonly_fields = ('imagen_preview',)
    fields = (
        'nombre',
        'descripcion',
        'precio',
        'stock',
        'porcion',
        'imagen',
        'imagen_preview',
    )

    @admin.display(description='Vista previa')
    def imagen_preview(self, obj):
        if obj is None:
            return 'Guarda el producto para ver la vista previa.'
        if not obj.imagen:
            return 'Sin imagen'
        return format_html(
            '<img src="{}" alt="{}" style="max-width: 180px; max-height: 120px; object-fit: contain;">',
            obj.imagen.url,
            obj.nombre,
        )

    @admin.display(description='Precio', ordering='precio')
    def precio_formateado(self, obj):
        precio = format(obj.precio, ',.2f')
        precio = precio.translate(str.maketrans('..', '..'))
        return f'${precio}'


@admin.register(encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'producto')
    search_fields = ('nombre', 'correo', 'telefono', 'producto__nombre')
