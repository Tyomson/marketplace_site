from django.test import TestCase
from django.contrib.auth.models import User
from app_products.models import Products, Profile, Marketplace

TEST_WORD = 'TestNew'
PASSWORD = 'TestPassword123'
TEST_NUMBER = 10.0


class MarketplaceModelsTest(TestCase):
    def test_add_new_marketplace(self):
        new_marketplace = Marketplace.objects.create(name=TEST_WORD)
        select_marketplace = Marketplace.objects.get(name=TEST_WORD)
        self.assertEqual(new_marketplace, select_marketplace)


class ProfileModelsTest(TestCase):
    def test_add_new_user(self):
        user = User.objects.create(username=TEST_WORD)
        new_user = Profile.objects.create(user=user)
        select_user = Profile.objects.get(user=user)
        self.assertEqual(new_user, select_user)


class ProductModelsTest(TestCase):
    def test_add_new_product(self):
        new_product = Products.objects.create(
            product_name=TEST_WORD,
            stocks=TEST_NUMBER,
            price=TEST_NUMBER
        )
        select_product = Products.objects.get(product_name=TEST_WORD)
        self.assertEqual(new_product, select_product)
