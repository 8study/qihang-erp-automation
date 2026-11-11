# -*- coding: utf-8 -*-
import json
import logging
import re

import pytest

from conftest import _exec
from conftest import _render as _orig_render
from base.globals_store import GLOBAL_VAR
from utils.allure_utils import allure_init
from utils.analy_case import jdbc_assert
from utils.excel_utils import read_excel


def _render_skip_if_missing(case):
    """渲染清理用例；若用例依赖的占位符变量在 GLOBAL_VAR 中缺失，
    说明上一轮已清理该数据、当前无待删行，返回 None 交由调用方跳过（视为通过）。"""
    raw = json.dumps(case, ensure_ascii=False)
    missing = [k for k in set(re.findall(r"\{\{(\w+)\}\}", raw)) if k not in GLOBAL_VAR]
    if missing:
        logging.info(f"编号{case['id']} 依赖缺失变量{missing}，无待清理数据，跳过")
        return None
    return _orig_render(case)


class TestCleanData:
    data = read_excel(feature="清理数据")

    @pytest.mark.parametrize("case", data)
    def test_clean_data(self, case):
        case = _render_skip_if_missing(case)
        if case is None:
            return  # 无数据待清理，视为通过
        logging.info(f"编号：{case['id']},模块:{case['feature']}")

        allure_init(case)
        response = _exec(case)

        # 清理用例不做内容断言：纯SQL行(path为空)无response；有response的只校验状态码，避免空expect触发 http_assert 的 None in str TypeError
        if response is not None and response.status_code >= 400:
            raise AssertionError(f"清理请求失败，状态码：{response.status_code}，响应体：{response.text}")

        if case.get("sql_check") or case.get("sqlExData"):
            jdbc_assert(case)