import logging

import pytest

from conftest import _render, _exec
from utils.allure_utils import allure_init
from utils.analy_case import http_assert, jdbc_assert
from utils.excel_utils import read_excel


class TestGoodsCategory:
    data = read_excel(feature="商品分类")

    @pytest.mark.parametrize("case", data)
    def test_goods_category(self, case):
        case = _render(case)
        logging.info(f"编号：{case['id']},模块:{case['feature']}")

        allure_init(case)
        response = _exec(case)

        http_assert(case, response)

        if case.get("sql_check") or case.get("sqlExData"):
            jdbc_assert(case)