import json

import pytest
from jinja2 import Template

from base.globals_store import GLOBAL_VAR 
from utils.allure_utils import allure_init
from utils.analy_case import *
from utils.excel_utils import read_excel

class TestLogin:
    data = read_excel(feature="登录")

    @pytest.mark.parametrize("case", data)
    def test_login(self, case):

        case = json.loads(Template(json.dumps(case)).render(GLOBAL_VAR))

        logging.info(f"编号：{case['id']},模块:{case['feature']}")

        allure_init(case)
        request_data = analy_case(case)
        response = send_http_request(**request_data)

        http_assert(case, response)
