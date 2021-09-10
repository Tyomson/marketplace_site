from django.test import TestCase
from django.urls import reverse
from app_products.forms import ExtendedRegisterForm, AddProduct

TEST_WORD = 'Test'
PASSWORD = 'TestPassword123'
TEST_NUMBER = 10.0


class ExtendedRegisterFormTest(TestCase):
    def test_register_form_date_field_label(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': TEST_WORD,
                'password': PASSWORD,
             }
        )
        self.assertEqual(response.status_code, 200)

    def test_form_is_valid(self):
        form_dict = {
            'username': TEST_WORD,
            'first_name': TEST_WORD,
            'last_name': TEST_WORD,
            'password1': PASSWORD,
            'password2': PASSWORD,
        }
        form = ExtendedRegisterForm(form_dict)
        self.assertTrue(form.is_valid())


class AddProductTest(TestCase):
    def test_form_is_valid(self):
        post_dict = {
            'product_name': TEST_WORD,
            'stocks': TEST_NUMBER,
            'price': TEST_NUMBER,
        }
        form = AddProduct(post_dict)
        self.assertTrue(form.is_valid())
