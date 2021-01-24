
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class PageOne(BasePage):

    url = "http://127.0.0.1/Home/User/index.html"
    user = "wangjinliang@qq.com"
    pwd = "123456"
    # 需要的页面元素对象
    user_input = (By.ID, 'username')
    pwd_input = (By.ID, 'password')
    code_input = (By.ID, 'verify_code')
    login_btn = (By.XPATH, '//*[@name="sbtbutton"]')

    # menu_bar = (By.XPATH, '//span[text()="啊哈哈哈"]')
    # ac_ob = (By.XPATH, '//span[text()="啊哈哈哈"]')
    # add_ac = (By.XPATH, '//span[text()="啊哈哈哈"]')
    # all_edit = (By.XPATH, '//tr[@class="el-table__row"][1]/td[last()]/div/button[1]')

    # 初始化浏览器
    def __init__(self, broswer_type, url=url):
        BasePage.__init__(self, broswer_typegit add, url)

    # *************************页面的操作*********************

    def login(self):
        self.locator_input(self.user_input, self.user)
        self.locator_input(self.pwd_input, self.pwd)
        self.locator_click(self.login_btn)
    # def select_menu(self):
    #     self.hover_and_click(self.menu_bar, self.ac_ob)
    #
    # def add_acpro_btn(self):
    #     self.locator_click(self.add_ac)
    #
    # def input_type(self, text):
    #     self.locator_input(self.all_edit, text)
    '''
    1.创建当前页面类，继承基本页面的类中的所有方法
    2.写出当前页面需要的元素对象
    3.写出当前页面的操作。即通过继承父类的方法，再结合当前页面已有的元素对象，写出对每个元素可进行的操作（点击，输入.....）。
    4.第3步完成，相当于当前页面对每个元素的操作都完成了。后续可新建模块，继承当前模块，通过有序的调用当前已有的操作方法。
        来模拟当前页面的各种操作场景
    '''