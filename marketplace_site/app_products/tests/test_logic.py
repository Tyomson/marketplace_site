from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from app_products.models import Products

TEST_WORD = 'TestWordLogic'
PASSWORD = 'TestPassword123'
TEST_NUMBER = 10.0


class LogicTest(TestCase):
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
        self.assertTrue(self.client.login(username=TEST_WORD, password=PASSWORD))

    def test_create_product_new(self):
        response = self.client.post(
            reverse('create_new_products'),
            {
                'product_name': TEST_WORD,
                'stocks': TEST_NUMBER,
                'price': TEST_NUMBER,
            }
        )
        self.assertEqual(response.status_code, 302)
        product = Products.objects.get(product_name=TEST_WORD)
        self.assertTrue(product)

