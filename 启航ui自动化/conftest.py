import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from locators_helper import dialog_close
from page.goods_base_data import GoodsBaseData
from page.page_login import PageLogin
from tools import Tools


def close_onboarding(driver):
    """登录后容错关闭"新手引导"弹窗：弹出则点右上角❌并等遮罩消失，未弹出则跳过
    注意：弹窗是登录成功跳转首页后才渲染的，要留足出现时间；
    轮询期间临时关掉隐式等待（否则 find 不到会阻塞 10s 再抛异常，把短超时架空）
    :param driver: 浏览器 driver
    """
    loc = dialog_close(dialog_cls="onboarding-dialog")
    overlay = (By.CSS_SELECTOR, 'div.el-overlay-dialog')
    driver.implicitly_wait(0)
    try:
        # 最多等 10 秒：出现弹窗则点❌；勾选过"不再显示"则一直没弹窗、超时跳过
        el = WebDriverWait(driver, 10, poll_frequency=0.5).until(
            lambda d: d.find_element(*loc) if d.find_elements(*loc) else False)
        el.click()
        # 等弹窗遮罩消失，避免后续点击被 el-overlay-dialog 拦截
        WebDriverWait(driver, 5).until(
            lambda d: not any(e.is_displayed() for e in d.find_elements(*overlay)))
    except Exception:
        pass  # 未弹出/关闭失败则忽略（登录已成功可直接继续）
    finally:
        driver.implicitly_wait(10)


# 浏览器驱动
@pytest.fixture()
def brower():
    driver = Tools.get_driver()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    Tools.quit_driver()  # 用工具方法关闭并重置单例，避免残留已退出的驱动


# 登录前置：所有业务流程共用的 fixture
@pytest.fixture()
def login_brower(brower):
    """
    登录前置：跳转登录页并登录（admin / ******）
    :param brower: 浏览器 driver fixture
    :return: 已登录的浏览器 driver
    """
    page_login = PageLogin(brower)
    page_login.get_url()
    page_login.login("admin", "")
    close_onboarding(brower)  # 登录后关闭新手引导弹窗（有则关、无则跳过），作为流程前置
    return brower


@pytest.fixture()
def page_brower(brower):
    page_login = PageLogin(brower)
    page_login.get_url()
    return page_login

@pytest.fixture()
def goods_cleanup(login_brower):
    GoodsBaseData(login_brower).cleanup_data()
