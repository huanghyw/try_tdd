from django.test import TestCase


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': '一个新的待办事项'})
        self.assertIn('一个新的待办事项', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
