from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 张三听说有一个在线待办事项应用
        # 打开浏览器，访问这个应用的网址
        self.browser.get("http://localhost:8000")

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
        time.sleep(1)

        # 页面显示"1：买一件衣服"
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1：买一件衣服')

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
        time.sleep(1)

        # 页面再次刷新，"1：买一件衣服"和"2：买一条裤子"这两条备忘
        self.check_for_row_in_list_table('1：买一件衣服')
        self.check_for_row_in_list_table('2：买一条裤子')

        self.fail("Finish the test!")

        # 接下来检查网站到底能不能记住待办事项
        # 。。。


if __name__ == '__main__':
    unittest.main()
