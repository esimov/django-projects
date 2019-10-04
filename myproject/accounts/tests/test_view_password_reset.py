from django.contrib.auth.forms import PasswordResetForm
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User


class PasswordResetViewTest(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)

    def test_reset_page_exists(self):
        self.assertTrue(self.response.status_code, 200)

    def test_reset_page_contains_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_reset_page_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)


class SuccessfulPasswordResetTest(TestCase):
    def setUp(self):
        user_data = {
            'username': 'test_account',
            'email': 'test_account@example.com',
            'password': 'admin123'
        }
        User.objects.create_user(user_data)
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': user_data['email']})

    def test_reset_password_should_redirect(self):
        self.assertRedirects(self.response, reverse('password_reset_done'))

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))
