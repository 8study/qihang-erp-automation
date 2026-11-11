import pytest

from page.page_login import PageLogin
from script import log
from tools import Tools, read_json


class TestLogin:

    # 前后置条件
    def setup_method(self):
        driver = Tools.get_driver()
        self.page_login = PageLogin(driver)
        self.page_login.get_url()

    def teardown_method(self):
        Tools.quit_driver()

    @pytest.mark.parametrize("account,password,expect", read_json("login_data.json"))
    def test_login(self, account, password, expect):
        self.page_login.login(account, password)

        # 成功用例的预期结果是欢迎语，失败用例的预期结果是错误提示文案
        if account == expect:
            result = self.page_login.get_success_result()
        else:
            result = self.page_login.get_error_result()
        log.info(f"登录结果：{result}")
        assert expect in result