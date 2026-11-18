from django.test import TestCase

from django.urls import reverse

from .models import encargo, linea, producto


class CatalogoTests(TestCase):
    def setUp(self):
        self.linea = linea.objects.create(nombre='Tortas')
        self.disponible = producto.objects.create(
            nombre='Torta de frutilla',
            linea=self.linea,
            descripcion='Bizcocho con crema y frutillas frescas.',
            precio='18000.00',
            stock=3,
            porcion='8 porciones',
        )
        self.agotado = producto.objects.create(
            nombre='Torta de chocolate',
            linea=self.linea,
            descripcion='Bizcocho de chocolate con ganache.',
            precio='20000.00',
            stock=0,
            porcion='10 porciones',
        )

    def test_catalogo_muestra_productos(self):
        response = self.client.get(reverse('catalogo'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.disponible.nombre)
        self.assertContains(response, self.agotado.nombre)
        self.assertContains(response, 'Agotado por hoy')
        self.assertContains(
            response,
            reverse('crear_encargo', args=[self.disponible.pk]),
        )
        self.assertContains(response, 'css/catalogo.css')

    def test_detalle_de_producto_disponible(self):
        response = self.client.get(
            reverse('detalle_producto', args=[self.disponible.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.disponible.nombre)

    def test_producto_disponible_abre_formulario_de_encargo(self):
        response = self.client.get(
            reverse('crear_encargo', args=[self.disponible.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Encargar Torta de frutilla')

    def test_formulario_crea_encargo_para_producto(self):
        response = self.client.post(
            reverse('crear_encargo', args=[self.disponible.pk]),
            {
                'nombre': 'Ana Pérez',
                'correo': 'ana@example.com',
                'telefono': '+56912345678',
                'fecha_retiro': '2026-11-20',
                'cantidad': 2,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comprobante de encargo')
        self.assertContains(response, '<dd>2</dd>', html=True)
        self.assertContains(response, 'CLP $36')
        self.assertContains(response, '20/11/2026')
        nuevo_encargo = encargo.objects.get(
            nombre='Ana Pérez',
            producto=self.disponible,
        )
        self.assertEqual(nuevo_encargo.fecha_retiro.isoformat(), '2026-11-20')
        self.assertEqual(nuevo_encargo.total, 36000)
        self.disponible.refresh_from_db()
        self.assertEqual(self.disponible.stock, 1)

    def test_formulario_muestra_stock_disponible_si_cantidad_se_excede(self):
        response = self.client.post(
            reverse('crear_encargo', args=[self.disponible.pk]),
            {
                'nombre': 'Ana Pérez',
                'correo': 'ana@example.com',
                'telefono': '+56912345678',
                'fecha_retiro': '2026-11-20',
                'cantidad': 4,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Solo hay 3 unidades disponibles.')
        self.assertFalse(encargo.objects.exists())

    def test_formulario_acepta_cantidad_mayor_a_tres_si_hay_stock(self):
        self.disponible.stock = 5
        self.disponible.save(update_fields=['stock'])

        response = self.client.post(
            reverse('crear_encargo', args=[self.disponible.pk]),
            {
                'nombre': 'Ana Pérez',
                'correo': 'ana@example.com',
                'telefono': '+56912345678',
                'fecha_retiro': '2026-11-20',
                'cantidad': 4,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Comprobante de encargo')
        self.disponible.refresh_from_db()
        self.assertEqual(self.disponible.stock, 1)

    def test_producto_agotado_no_puede_encargarse(self):
        response = self.client.get(
            reverse('crear_encargo', args=[self.agotado.pk]),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Agotado por hoy')
        self.assertFalse(encargo.objects.exists())

    def test_fecha_de_retiro_es_obligatoria(self):
        response = self.client.post(
            reverse('crear_encargo', args=[self.disponible.pk]),
            {
                'nombre': 'Ana Pérez',
                'correo': 'ana@example.com',
                'telefono': '+56912345678',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fecha de retiro')
        self.assertFalse(encargo.objects.exists())

    def test_detalle_de_producto_agotado_muestra_aviso(self):
        response = self.client.get(
            reverse('detalle_producto', args=[self.agotado.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Agotado por hoy')
        self.assertNotContains(
            response,
            reverse('crear_encargo', args=[self.agotado.pk]),
        )

    def test_producto_inexistente_muestra_error_404(self):
        response = self.client.get(reverse('detalle_producto', args=[9999]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Volver al catálogo', status_code=404)
