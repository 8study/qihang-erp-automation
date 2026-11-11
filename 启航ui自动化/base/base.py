import os.path
import time

from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import PATH
from tools import GetLog


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def fd_element(self, locator):
        """
        查找元素
        :param locator: 元素定位方式及属性值
        :return: 元素对象
        """
        try:
            element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))
            return element
        except Exception as e:
            GetLog.get_log().error(f"查找元素失败：{locator}, 错误原因：{e}")
            raise

    def base_input(self, locator, text):
        """
        输入操作
        :param locator: 元素定位方式及属性值
        :param text: 输入文本
        """
        ele = self.fd_element(locator)
        ele.clear()
        ele.send_keys(text)

    def base_click(self, locator):
        """
        点击操作
        :param locator: 元素定位方式及属性值
        """
        self.fd_element(locator).click()
        time.sleep(1)

    def get_shot(self, file_name):
        """
        截图操作
        :param file_name: 截图文件名
        """
        file_path = os.path.join(PATH, "img", file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.driver.get_screenshot_as_file(file_path)

    def base_switch_handle(self, locator):
        """
        切换窗口操作并获取指定元素
        :param locator: 元素定位方式及属性值
        :return: 切换窗口后的元素对象
        """
        WebDriverWait(self.driver, self.timeout).until(lambda x: len(x.window_handles) > 1)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

        element = self.fd_element(locator)
        return element

    def base_switch_frame(self, locator):
        """
        切换frame操作
        :param locator: frame定位方式及属性值
        """
        frame_ele = self.fd_element(locator)
        self.driver.switch_to.frame(frame_ele)

    def base_default_content(self):
        """
        切换回默认内容操作
        """
        self.driver.switch_to.default_content()

    def base_clear(self, locator, num):
        """
        输入前，先清空操作
        :param locator: 元素定位方式及属性值
        :param num: 数字
        :return:
        """
        ele = self.fd_element(locator)
        ele.click()
        ele.send_keys(Keys.CONTROL, "a")  # 全选 0.00
        ele.send_keys(num)

    @staticmethod
    def sql_clean(SQL, conn):
        """执行清理 SQL（只执行不关连接，连接由调用方负责开/关）
        :param SQL: 要依次执行的 SQL 列表
        :param conn: pymysql 连接
        """
        # conn 是 config.py 里的全局单例，被某个用例 teardown_method 的 conn.close() 关掉后
        # 后续用例仍在复用它，会抛 InterfaceError(0,'')；每次执行前 ping 一下自动重连
        conn.ping(reconnect=True)
        with conn.cursor() as cursor:
            for sql in SQL:
                cursor.execute(sql)
        conn.commit()

    def get_success_result(self, success_res):
        """
        获取成功结果
        :param success_res: 成功结果定位方式及属性值
        :return: 成功结果文本
        """
        return self.fd_element(success_res).text
