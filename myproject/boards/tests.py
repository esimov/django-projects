from django.test import TestCase
from django.urls import reverse

from .models import Board, Topic


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

    def test_new_topic_view_contains_link_back_to_board_topics(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(new_topic_url)
        boards_url = reverse('topics', kwargs={'pk': self.board.pk})
        self.assertContains(response, 'href="{0}"'.format(boards_url))

    def test_csrf(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.get(new_topic_url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_new_post_content_is_valid(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})
        data = {
            'subject': 'Dummy Title',
            'message': 'Dummy Message'
        }
        response = self.client.post(
            new_topic_url, data=data, content_type='application/x-www-form-urlencoded')

    def test_new_post_content_not_empty(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        new_topic_url = reverse('new_topic', kwargs={'pk': self.board.pk})
        response = self.client.post(
            new_topic_url, data={'subject': '', 'message': ''}, content_type='application/x-www-form-urlencoded')
        self.assertTrue(response.status_code, 200)
