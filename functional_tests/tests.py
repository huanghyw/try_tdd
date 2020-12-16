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

    def test_can_start_a_list_for_one_user(self):
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

        # 他很满意，去睡觉了

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 张三新建一个待办事项
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('买一瓶可乐')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1：买一瓶可乐')

        # 他看见清单有一个唯一的URL
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url, '/lists/.+')

        # 现在李四访问了网站

        ## 我们使用一个新的浏览器回话
        ## 确保张三的信息不会从Cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 李四访问首页
        # 页面中看不到张三的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买一瓶可乐', page_text)
        self.assertNotIn('买一件衣服', page_text)

        # 李四输入一个新的待办事项，新建一个清单
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('买一个气球')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1：买一个气球')

        # 李四获得了他的一个唯一URL
        lisi_list_url = self.browser.current_url
        self.assertRegex(lisi_list_url, '/lists/.+')
        self.assertNotEqual(lisi_list_url, zhangsan_list_url)

        # 这个页面没有张三的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('买一瓶可乐', page_text)
        self.assertIn('买一个气球', page_text)

        # 两个人都很满意，然后去睡觉了

        # 。。。

        # 页面中有一些解说性的文字
        self.fail("Finish the test!")