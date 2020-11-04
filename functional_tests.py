from selenium import webdriver

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
        self.fail("Finish the test!")

        # 他尝试着输入一个待办事项
        # 。。。


if __name__ == '__main__':
    unittest.main()
