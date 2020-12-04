from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': '一个新的待办事项'})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '一个新的待办事项')

    def test_redirect_after_POST(self):
        response = self.client.post('/', data={'item_text': '一个新的待办事项'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_displays_all_list_items(self):
        Item.objects.create(text='第一项')
        Item.objects.create(text='第二项')

        response = self.client.get('/')

        self.assertIn('第一项', response.content.decode())
        self.assertIn('第二项', response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = '第一条待办'
        first_item.save()

        second_item = Item()
        second_item.text = '第二条待办'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '第一条待办')
        self.assertEqual(second_saved_item.text, '第二条待办')
