from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

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
        self.assertTrue(
            any(row.text == '1:买一件衣服' for row in rows),
            '新添加的待办事项保存失败'
        )

        # 页面又显示了一个文本框，可以输入其它待办事项
        # 他输入了"买一条裤子"
        self.fail("Finish the test!")

        # 页面再次刷新，他的清单中显示了这两个待办事项
        # 。。。


if __name__ == '__main__':
    unittest.main()
