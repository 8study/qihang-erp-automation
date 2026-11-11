from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.base import BasePage
from config import BASE_URL
from tools import Tools


class PageLogin(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.account = (By.XPATH, '//input[@placeholder="账号/手机号"]')
        self.password = (By.XPATH, '//input[@placeholder="密码"]')
        self.login_btn = (By.CSS_SELECTOR, 'button.el-button--primary')

        self.success_result = (By.CSS_SELECTOR, 'span.user-name')
        self.toast_frame = (By.CSS_SELECTOR, 'p.el-message__content')
        self.form_error_username = (
        By.XPATH, '//div[contains(@class,"el-form-item__error")][contains(text(),"请输入您的账号")]')
        self.form_error_password = (
        By.XPATH, '//div[contains(@class,"el-form-item__error")][contains(text(),"请输入您的密码")]')

    def get_url(self):
        self.driver.get(BASE_URL + "/login?redirect=/index")

    def login(self, account, password):
        self.base_input(self.account, account)

        self.base_input(self.password, password)

        self.base_click(self.login_btn)

    def get_success_result(self):
        return self.fd_element(self.success_result).text

    def get_error_result(self):
        """获取错误提示：同时监听 toast 与表单校验错误，谁先出现返回谁"""
        locators = (self.toast_frame, self.form_error_username, self.form_error_password)

        def _found(driver):
            for locator in locators:
                try:
                    ele = driver.find_element(*locator)
                    if ele.is_displayed():
                        return ele.text
                except Exception:
                    continue
            return False

        return WebDriverWait(self.driver, 3).until(_found)


if __name__ == '__main__':
    login = PageLogin(Tools.get_driver())
    login.get_url()
    login.login("admin", "")
