
import time
from pages.page_login import PageOne
import pytest
import os


screenshots_path = "../screenshot/"

print(os.path.abspath(screenshots_path))


class TestPageOne(object):

    def setup(self):
        self.page_one = PageOne("chrome")

    def teardown(self):
        self.page_one.quit()

    def test01(self):
        page_one = self.page_one
        page_one.screenshots_png(screenshots_path)
        page_one.verify_code_png()
        page_one.login()

        # page_one.select_menu()
        # page_one.add_acpro_btn()
        time.sleep(2)
        # page_one.input_type(text)


if __name__ == '__main__':

    pytest.main(['test_one.py', '-q'])
    '''
    1.初始化
    2.导入具体的页面模块，通过调用模块的方法，调整方法的顺序，模拟页面不同的操作场景，写出多个case
    '''
