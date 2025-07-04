from django.test import TestCase

from .models import Category, Product


class CategoryModelTestCase(TestCase):
    """Tests for Model Category"""

    def setUp(self):
        self.category = Category.objects.create(name='T-shirts', slug='t-shirts')

    def test_creation_category(self):
        self.assertEqual(self.category.name, 'T-shirts')
        self.assertEqual(self.category.slug, 't-shirts')
        self.assertIsInstance(self.category, Category)

    def test_category_slug_unique(self):
        self.assertEqual(str(self.category.slug), 't-shirts')


class ProductModelTestCase(TestCase):
    """Tests for Product Model"""

    def setUp(self):
        self.category = Category.objects.create(name='T-shirts', slug='t-shirts')
        self.product = Product.objects.create()

    def test_creation_product(self):
        pass

    def test_product_percent_validation(self):
        pass


class CatalogViewTestCase(TestCase):
    pass
