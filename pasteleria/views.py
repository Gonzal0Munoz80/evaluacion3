from django.db import transaction
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EncargoForm
from .models import linea, producto


def catalogo(request):
    productos = producto.objects.filter(
        visible_en_catalogo=True,
    ).select_related('linea')

    busqueda = request.GET.get('q', '').strip()
    linea_id = request.GET.get('linea', '')
    linea_seleccionada = None

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
            | Q(linea__nombre__icontains=busqueda)
        )

    if linea_id.isdigit():
        linea_seleccionada = int(linea_id)
        productos = productos.filter(linea_id=linea_seleccionada)

    productos = productos.order_by('linea__nombre', 'nombre')
    lineas = linea.objects.order_by('nombre')
    return render(
        request,
        'pasteleria/catalogo.html',
        {
            'productos': productos,
            'lineas': lineas,
            'busqueda': busqueda,
            'linea_seleccionada': linea_seleccionada,
        },
    )


def detalle_producto(request, producto_id):
    producto_actual = producto.objects.filter(
        pk=producto_id,
        visible_en_catalogo=True,
    ).first()
    if producto_actual is None:
        return render(request, 'pasteleria/404.html', status=404)

    return render(
        request,
        'pasteleria/detalle_producto.html',
        {'producto': producto_actual},
    )


def crear_encargo(request, producto_id):
    producto_actual = get_object_or_404(
        producto,
        pk=producto_id,
        visible_en_catalogo=True,
    )
    if producto_actual.stock <= 0:
        return redirect('detalle_producto', producto_id=producto_actual.pk)

    enviado = False
    encargo_creado = None
    if request.method == 'POST':
        form = EncargoForm(request.POST, producto=producto_actual)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            with transaction.atomic():
                stock_actualizado = producto.objects.filter(
                    pk=producto_actual.pk,
                    stock__gte=cantidad,
                ).update(stock=F('stock') - cantidad)

                if stock_actualizado:
                    nuevo_encargo = form.save(commit=False)
                    nuevo_encargo.producto = producto_actual
                    nuevo_encargo.precio_unitario = producto_actual.precio
                    nuevo_encargo.save()
                    enviado = True
                    encargo_creado = nuevo_encargo
                else:
                    producto_actual.refresh_from_db(fields=['stock'])
                    form.add_error(
                        'cantidad',
                        f'Solo hay {producto_actual.stock} unidades disponibles.',
                    )
    else:
        form = EncargoForm(producto=producto_actual)

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
