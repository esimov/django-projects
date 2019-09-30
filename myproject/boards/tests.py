from django.test import TestCase
from django.urls import reverse


class BoardsIndexViewTests(TestCase):
    def test_index_status_code(self):
        """
        If no boards exists, and appropiate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertContains(response, "No boards are available.")
        self.assertEqual(response.status_code, 200)
