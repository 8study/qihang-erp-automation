# -*- coding: utf-8 -*-
import json
import logging

import pytest
from jinja2 import Template

from base.globals_store import GLOBAL_VAR
from utils.analy_case import analy_case, send_http_request, json_extract, jdbc_extract
from utils.excel_utils import read_excel


def _render(case):
    """用 GLOBAL_VAR 渲染用例中的 {{占位符}}"""
    return json.loads(Template(json.dumps(case)).render(GLOBAL_VAR))


def _exec(case):
    """执行单个用例：发送请求 + json/jdbc 提取变量到 GLOBAL_VAR。

    path 为空的用例行视为纯 SQL 清理用例（method/url 缺失），跳过 HTTP，
    仅执行 sql_check/sqlExData；有 path 的正常发 HTTP。返回响应（SQL 用例返回 None）。
    """
    if case.get("path"):
        request_data = analy_case(case)
        response = send_http_request(**request_data)
        json_extract(case, GLOBAL_VAR, response)
    else:
        logging.info("SQL清理用例：path为空，跳过HTTP，仅执行SQL")
        response = None
    jdbc_extract(case, GLOBAL_VAR)
    return response


@pytest.fixture(scope="session", autouse=True)
def login_setup():
    """
    会话级前置：登录并提取 token。

    """
    if GLOBAL_VAR.get("TOKEN"):
        yield
        return

    # 取登录链路用例（登录 + 获取用户信息 + 获取路由）执行，提取 TOKEN 等变量
    for case in read_excel():
        # 清理数据feature的纯SQL行 path为None，需判空避免 AttributeError
        if case.get("path") and (case["path"].startswith("/passport/member/userLogin") or case["path"].startswith("/sys-api/get")):
            _exec(_render(case))

    yield


# conftest.py —— 第一个钩子:注册 --feature 参数
def pytest_addoption(parser):
    parser.addoption("--feature", action="store", default=None,
                     help="只执行指定 feature 的用例")


# 第二个钩子:收集完按 feature 精确筛掉其它用例
def pytest_collection_modifyitems(session, config, items):
    feature = config.getoption("--feature")
    if not feature:
        return
    keep = []
    for item in items:
        case = item.callspec.params.get("case", None)
        # 和 feature 完全相等才留,其它全删
        if case and case.get("feature") == feature:
            keep.append(item)
    items[:] = keep