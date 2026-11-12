from django.shortcuts import get_object_or_404, render

from .forms import EncargoForm
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


def crear_encargo(request, producto_id):
    producto_actual = get_object_or_404(producto, pk=producto_id)
    if producto_actual.stock <= 0:
        return render(request, 'pasteleria/404.html', status=404)

    enviado = False
    encargo_creado = None
    if request.method == 'POST':
        form = EncargoForm(request.POST)
        if form.is_valid():
            nuevo_encargo = form.save(commit=False)
            nuevo_encargo.producto = producto_actual
            nuevo_encargo.save()
            enviado = True
            encargo_creado = nuevo_encargo
    else:
        form = EncargoForm()

    return render(
        request,
        'pasteleria/encargo.html',
        {
            'producto': producto_actual,
            'form': form,
            'enviado': enviado,
            'encargo_creado': encargo_creado,
        },
    )
