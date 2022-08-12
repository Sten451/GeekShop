from django.test import TestCase
from mainapp.models import ProductCategory, Product
from django.test.client import Client


class TestMainSmokeTest(TestCase):
    status_code_success = 200

    def setUp(self) -> None:
        category = ProductCategory.objects.create(name='Test')
        Product.objects.create(category=category, name='product_test', price=100)
        Product.objects.create(category=category, name='product_test2', price=120)
        Product.objects.create(category=category, name='product_test3', price=150)
        self.client = Client()

    def tearDown(self) -> None:
        pass

    def test_products_basket(self):
        response = self.client.get('/users/profile')
        self.assertEqual(response.status_code, 302)

    def test_products_product(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/detail/{product_item.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)
