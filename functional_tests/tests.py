from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 张三听说有一个在线待办事项应用
        # 打开浏览器，访问这个应用的网址
        self.browser.get(self.live_server_url)

        # 他发现标题包含待办事项这四个字
        self.assertIn("待办事项", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('待办事项', header_text)

        # 应用邀请她输入一个待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            '输入一个待办事项'
        )

        # 他在一个文本框中输入了"买一件衣服"
        input_box.send_keys("买一件衣服")
        # 输入完成后，按回车，页面刷新
        input_box.send_keys(Keys.ENTER)

        # 页面显示"1：买一件衣服"
        self.wait_for_row_in_list_table('1：买一件衣服')

        # 页面又显示了一个文本框，可以输入其它待办事项
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            '输入一个待办事项'
        )

        # 他输入了"买一条裤子"
        input_box.send_keys("买一条裤子")
        # 输入完成后，按回车，页面刷新
        input_box.send_keys(Keys.ENTER)

        # 页面再次刷新，"1：买一件衣服"和"2：买一条裤子"这两条备忘
        self.wait_for_row_in_list_table('1：买一件衣服')
        self.wait_for_row_in_list_table('2：买一条裤子')

        self.fail("Finish the test!")

        # 接下来检查网站到底能不能记住待办事项
        # 。。。
