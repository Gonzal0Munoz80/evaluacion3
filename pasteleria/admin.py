from django.contrib import admin
from django.utils.html import format_html

from .models import producto, encargo


# Register your models here.
class DisponibilidadFilter(admin.SimpleListFilter):
    title = 'Disponibilidad'
    parameter_name = 'disponibilidad'

    def lookups(self, request, model_admin):
        return (
            ('disponible', 'Disponible'),
            ('agotado', 'Agotado por hoy'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'disponible':
            return queryset.filter(stock__gt=0)
        if self.value() == 'agotado':
            return queryset.filter(stock__lte=0)
        return queryset


@admin.register(producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'descripcion',
        'precio_formateado',
        'stock',
        'disponibilidad',
        'porcion',
        'imagen_preview',
    )
    list_filter = (DisponibilidadFilter,)
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

    @admin.display(description='Disponibilidad', ordering='stock')
    def disponibilidad(self, obj):
        if obj.stock <= 0:
            return 'Agotado por hoy'
        return 'Disponible'


@admin.register(encargo)
class EncargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'producto', 'fecha_retiro')
    search_fields = ('nombre', 'correo', 'telefono', 'producto__nombre')
