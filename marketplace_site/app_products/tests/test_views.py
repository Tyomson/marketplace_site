from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from app_products.models import Marketplace, Products, ShoppingCart

TEST_WORD = 'TestWord'
PASSWORD = 'TestPassword123'


class ProductViewTest(TestCase):
    def test_product_view_url_exists_at_desired_location(self):
        response = self.client.get('/products/products_list/')
        self.assertEqual(response.status_code, 200)

    def test_product_view_uses_correct_template(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_products/products_list.html')


class CreateProductTest(TestCase):
    def test_create_product_url_exists_at_desired_location(self):
        response = self.client.get('/products/create_new_products/')
        self.assertEqual(response.status_code, 200)

    def test_create_product_view_uses_correct_template(self):
        response = self.client.get(reverse('create_new_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_products/create_new_products.html')


class RegisterTest(TestCase):
    def test_register_url_exists_at_desired_location(self):
        response = self.client.get('/products/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_products/register.html')

    def test_create_new_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': TEST_WORD,
                'password1': PASSWORD,
                'password2': PASSWORD,
            }
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username=TEST_WORD)
        self.assertTrue(user)

    def test_create_new_user_failed(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': TEST_WORD,
                'password1': PASSWORD,
                'password2': TEST_WORD,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_products/register.html')


class AnotherLoginTest(TestCase):
    def test_login_view_url_exists_at_desired_location(self):
        response = self.client.get('/products/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get('/products/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_products/login.html')


class AccountViewTest(TestCase):
    def test_account_view_url_exists_at_desired_location(self):
        response = self.client.get('/products/account/')
        self.assertEqual(response.status_code, 200)

    def test_account_view_uses_correct_template(self):
        response = self.client.get('/products/account/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_products/account.html')


