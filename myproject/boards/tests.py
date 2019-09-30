from django.test import TestCase
from django.urls import reverse

from .models import Board


class BoardsIndexViewTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(
            name="Python Board", description="General Python discussion board")
        self.response = self.client.get(reverse('index'))

    def test_index_status_code(self):
        """
        If no boards exists, and appropiate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_contains_links_to_topics(self):
        topics_url = reverse('topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(topics_url))

    def test_topics_contains_link_to_home(self):
        board_topics_url = reverse('topics', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        home_page_url = reverse('index')
        self.assertContains(response, 'href="{0}"'.format(home_page_url))
