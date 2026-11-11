import logging

import pytest

from base.globals_store import GLOBAL_VAR
from conftest import _render, _exec
from utils.allure_utils import allure_init
from utils.analy_case import http_assert, jdbc_assert
from utils.excel_utils import read_excel


class TestCreateShopOrder:
    data = read_excel(feature="订单库")

    @pytest.mark.parametrize("case", data)
    def test_create_shop_order(self, case):
        case = _render(case)
        logging.info(f"编号：{case['id']},模块:{case['feature']}")

        allure_init(case)
        response = _exec(case)

        http_assert(case, response)

        if case.get("sql_check") or case.get("sqlExData"):
            jdbc_assert(case)

        print(f"GLOBAL_VAR: {GLOBAL_VAR}")
