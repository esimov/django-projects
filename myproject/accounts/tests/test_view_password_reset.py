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
        email = 'john.doe@example.com'
        User.objects.create_user(
            username='john.doe', email=email, password='admin123')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_reset_password_should_redirect(self):
        self.assertRedirects(self.response, reverse('password_reset_done'))

    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTest(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(
            url, {'email': 'invalid_user_account@example.com'})

    def test_reset_password_should_redirect(self):
        self.assertRedirects(self.response, reverse('password_reset_done'))

    def test_password_reset_send_email_failed(self):
        self.assertEqual(0, len(mail.outbox))


class PasswordResetDoneTest(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_password_reset_done_should_exists(self):
        self.assertEqual(self.response.status_code, 200)
