import json
import os
import logging
from selenium import webdriver
import time
from logging import handlers
from config import PATH


class Tools:
    driver = None

    @classmethod
    def get_driver(cls):
        """获取浏览器对象"""
        if cls.driver is None:
            cls.driver = webdriver.Edge()
            cls.driver.maximize_window()
            # cls.driver.implicitly_wait(10)
        return cls.driver

    @classmethod
    def quit_driver(cls):
        """关闭浏览器"""
        if cls.driver:
            time.sleep(1)
            cls.driver.quit()
            cls.driver = None

def read_json(file_name):
    """
    读取json文件，转换为列表
    :param file_name: 文件名
    :return: 列表[(),()...]
    """
    data=[]
    file_path=PATH+"/data/"+file_name
    with open(file_path,"r",encoding="utf-8") as f:
        tmp = json.load(f)
        for i in tmp:
            t = tuple(i.values())
            data.append(t)
        return data

class GetLog:
    # 日志器
    __log = None

    @classmethod
    def get_log(cls):
        if cls.__log is None:
            # 获取日志器
            cls.__log = logging.getLogger()
            # 设置入口级别
            cls.__log.setLevel(logging.INFO)
            # 获取处理器
            log_dir = os.path.join(PATH, "log")
            os.makedirs(log_dir, exist_ok=True)
            filename = os.path.join(log_dir, "web.log")
            tf = logging.handlers.TimedRotatingFileHandler(filename=filename,  # 日志文件名
                                                           when="midnight",  # 日志归档时间
                                                           interval=1,  # 每天归档一次
                                                           backupCount=3,  # 保留3天日志
                                                           encoding="utf-8")  # 日志编码格式
            # 获取格式器
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
            fm = logging.Formatter(fmt)
            # 将格式器添加到处理器
            tf.setFormatter(fm)
            # 将处理器添加到日志器
            cls.__log.addHandler(tf)
        # 返回日志器
        return cls.__log

if __name__ == '__main__':
    driver = Tools.get_driver()
    driver.get("https://www.baidu.com")
    Tools.quit_driver()