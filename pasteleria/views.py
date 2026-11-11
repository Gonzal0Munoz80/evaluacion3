from django.shortcuts import render

from .models import producto


def catalogo(request):
    productos = producto.objects.all().order_by('nombre')
    return render(request, 'pasteleria/catalogo.html', {'productos': productos})


def detalle_producto(request, producto_id):
    producto_actual = producto.objects.filter(pk=producto_id).first()
    if producto_actual is None or producto_actual.stock <= 0:
        return render(request, 'pasteleria/404.html', status=404)

    return render(
        request,
        'pasteleria/detalle_producto.html',
        {'producto': producto_actual},
    )
