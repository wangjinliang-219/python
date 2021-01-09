
import os
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from PIL import Image
import pytesseract
import time


class BasePage(object):
    shot_file = "../screenshots/"

    def __init__(self, broswer_type, url):
        self.driver = self.open_broswer(broswer_type)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.open_page(url)

    def open_broswer(self, broswer_type):
        if broswer_type.lower() == "chrome":
            option = webdriver.ChromeOptions()
            # option.add_experimental_option("excludeSwitches", ['enable-automation'])
            driver = webdriver.Chrome(chrome_options=option)
            return driver
        elif broswer_type.lower() == "firefox":
            pass

    def open_page(self, url):
        self.driver.get(url)

    def locator_el(self, locator_el, timeout=0.5):
        try:
            su_el = WebDriverWait(self.driver, timeout=timeout).until(
                    lambda el: self.driver.find_element(*locator_el))
            return su_el
        except Exception as e:
            print(e)

    def locator_els(self, locator_el):
        try:
            su_el = WebDriverWait(self.driver, timeout=timeout).until(
                lambda el: self.driver.find_elements(*locator_el))
            return su_el
        except Exception as e:
            print(e)

    def locator_input(self, locator_el, content):
        try:
            self.locator_el(locator_el).clear()
            self.locator_el(locator_el).send_keys(content)
        except Exception as e:
            print(e)

    def locator_click(self, locator_el):
        try:
            self.locator_el(locator_el).click()
        except Exception as e:
            print(e)

    def hover_and_click(self, locator_el, click_el):
        '''

        :param locator_el: hover的元素对象
        :param click_el:点击的元素对象
        :return:
        '''
        try:
            el = self.locator_el(locator_el)
            ActionChains(self.driver).move_to_element(el).perform()
            time.sleep(1)
            el2 = self.locator_el(click_el)
            ActionChains(self.driver).click(el2).perform()
        except Exception as e:
            print(e)

    def alter_accept(self, content=None):
        if content is None:
            try:
                alter_ob = self.driver.switch_to.alter
                alter_ob.accept()
                return alter_ob.text
            except Exception as e:
                print(e)
        else:
            try:
                alter_ob = self.driver.switch_to.alter
                alter_ob.send_keys(content)
                alter_ob.accept()
                return alter_ob.text
            except Exception as e:
                print(e)

    def alter_dismiss(self, content=None):
        if content is None:
            try:
                alter_ob = self.driver.switch_to.alter
                alter_ob.dismiss()
                return alter_ob.text
            except Exception as e:
                print(e)
        else:
            try:
                alter_ob = self.driver.switch_to.alter
                alter_ob.send_keys(content)
                alter_ob.dismiss()
                return alter_ob.text
            except Exception as e:
                print(e)

    def switch_handle(self, handle_title):
        handle_ob = self.driver.window_handles
        for window_tag in handle_ob:
            if window_tag == handle_title:
                self.driver.switch_to.window(window_tag)
                break

    def switch_default_handle(self):
        handle_ob = self.driver.window_handles
        self.driver.switch_to.window(handle_ob[0])

    def get_current_handle(self):
        current_handle = self.driver.current_window_handle
        return current_handle

    def switch_frame(self, locator_el):
        frame_el = self.locator_el(locator_el)
        self.driver.switch_to.frame(frame_el)

    def switch_to_default(self):
        self.driver.switch_to.default_content()

    def switch_to_parent(self):
        self.driver.switch_to.parent_frame()

        # 拖动

    def select_combobox_value(self, locator_el, value):
        selector = Select(self.locator_el(locator_el))
        selector.select_by_value(value)

    def select_combobox_index(self, locator_el, index):
        selector = Select(self.locator_el(locator_el))
        selector.select_by_index(index)

    def select_combobox_text(self, locator_el, text):
        selector = Select(self.locator_el(locator_el))
        selector.select_by_visible_text(text)

    def deselect_combobox_value(self, locator_el, se_value):
        selector = Select(self.locator_el(locator_el))
        selector.deselect_by_value(se_value)

    def deselect_combobox_index(self, locator_el, index):
        selector = Select(self.locator_el(locator_el))
        selector.deselect_by_index(index)

    def deselect_combobox_text(self, locator_el, text):
        selector = Select(self.locator_el(locator_el))
        selector.select_by_visible_text(text)

    def upload_file(self, locator_el, file_name):
        file = os.path.abspath(file_name)
        self.locator_el(locator_el).send_keys(file)

    def get_attribute(self, locator_el):
        attr = self.locator_el(locator_el).get_attribute()
        return attr

    def get_text(self, locator_el):
        text = self.locator_el(locator_el).text
        return text

    def get_size(self, locator_el, ):
        size = self.locator_el(locator_el).size
        return size

    def get_tag_name(self, locator_el):
        tag_name = self.locator_el(locator_el).tag_name
        return tag_name

    def time_format(self):
        current_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        return current_time

    def screenshots_png(self, filename="../screenshot/"):
        if not filename.endswith('/') or filename.endswith('\\'):
            filename = filename + "/"
        try:
            png_name = self.time_format() + ".png"
            self.driver.save_screenshot(filename + png_name)
            return png_name, filename
        except IOError:
            return False

    # def verify_code_png(self, locator_el):
    #     png_name, filename = self.screenshots_png()
    #
    #     verify_code = self.locator_el(locator_el)
    #     lelf = verify_code.location['x']
    #     top = verify_code.location['y']
    #     right = lelf + verify_code.size['width']
    #     height = top + verify_code.size['height']
    #
    #     im = Image.open(filename + png_name)
    #     img = im.crop((lelf, top, right, height))
    #     png_name_2 = self.time_format() + ".png"
    #     img.save(png_name_2)

    def click(self, el_obj):
        el_obj.click()

    def refresh(self):
        self.driver.refresh()

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def current_url(self):
        self.driver.current_url()

    def get_title(self):
        self.driver.title()

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()

    def add_cookie(self, cookie_dict):
        self.driver.add_cookie(cookie_dict)

    def get_cookies(self):
        self.driver.get_cookies()

    def get_cookie_name(self, name):
        self.driver.get_cookie(name)

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def delete_cookie(self, name):
        self.driver.delete_cookie(name)
