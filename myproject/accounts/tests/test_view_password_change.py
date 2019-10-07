from django.contrib.auth.forms import PasswordResetForm
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User


class PasswordChangeViewTest(TestCase):
    def setUp(self):
        self.url = reverse('password_change')
        self.response = self.client.get(self.url)

    def test_password_change_page_exists(self):
        self.assertTrue(self.response.status_code, 200)

    def test_password_change_should_redirect_if_not_logged_in(self):
        login_url = reverse('login')
        self.assertRedirects(
            self.response, '{0}?next={1}'.format(login_url, self.url))


class PasswordChangeTest(TestCase):
    def setUp(self, data={}):
        self.url = reverse('password_change')
        self.user = User.objects.create_user(
            username="john.doe", email='john.doe@example.com', password="old_password")
        self.client.login(username='john.doe', password='old_password')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTest):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_password_change_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_change_success(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_is_authenticated(self):
        home_page = self.client.get(reverse('index'))
        is_authenticated = home_page.context.get('user').is_authenticated
        self.assertEqual(is_authenticated, True)


class InvalidPasswordChange(PasswordChangeTest):
    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_password_change_failed(self):
        self.assertTrue(self.user.check_password('old_password'))
