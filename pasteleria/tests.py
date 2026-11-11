from django.test import TestCase

from django.urls import reverse

from .models import producto


class CatalogoTests(TestCase):
    def setUp(self):
        self.disponible = producto.objects.create(
            nombre='Torta de frutilla',
            descripcion='Bizcocho con crema y frutillas frescas.',
            precio='18000.00',
            stock=3,
            porcion='8 porciones',
        )
        self.agotado = producto.objects.create(
            nombre='Torta de chocolate',
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
        self.assertContains(response, 'css/catalogo.css')

    def test_detalle_de_producto_disponible(self):
        response = self.client.get(
            reverse('detalle_producto', args=[self.disponible.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.disponible.nombre)

    def test_detalle_de_producto_agotado_muestra_error_404(self):
        response = self.client.get(
            reverse('detalle_producto', args=[self.agotado.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Este pastel no está disponible', status_code=404)

    def test_producto_inexistente_muestra_error_404(self):
        response = self.client.get(reverse('detalle_producto', args=[9999]))

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, 'Volver al catálogo', status_code=404)
