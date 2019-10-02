from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..forms import SignupForm


class SignupTest(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_page_exists(self):
        signup_url = reverse('signup')
        response = self.client.get(signup_url)
        self.assertTrue(response.status_code, 200)

    def test_signup_contains_csrf(self):
        signup_url = reverse('signup')
        response = self.client.get(signup_url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignupForm)


class SuccessfulSignupTest(TestCase):
    def setUp(self):
        signup_url = reverse('signup')
        data = {
            'username': 'test_account',
            'password1': 'admin123',
            'password2': 'admin123',
        }
        self.response = self.client.post(signup_url, data)
        self.home_url = reverse('index')

    def test_redirect(self):
        self.assertRedirects(self.response, self.home_url)

    def test_post_is_valid(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        '''
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertContains(response, user)
        self.assertTrue(user.is_authenticated)


class InvalidSignupTest(TestCase):
    def setUp(self):
        signup_url = reverse('signup')
        self.response = self.client.post(signup_url, {})
        self.home_url = reverse('index')

    def test_signup_status_code(self):
        self.assertNotEqual(self.response, 200)

    def test_signup_form_error(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_user_creation_failed(self):
        self.assertFalse(User.objects.exists())
