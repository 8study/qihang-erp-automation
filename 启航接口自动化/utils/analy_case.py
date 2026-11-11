import json
import logging

import allure
import jsonpath
import pymysql
import requests

from config import *


@allure.step("解析请求数据")
def analy_case(case):
    """
    分析用例
    :param case: 测试用例
    :return: 请求数据
    """

    request_data = {
        "method": case["method"],
        "url": BASE_URL + case["path"],
        "params": case["params"] if case["params"] else None,
        "data": case["data"] if case["data"] else None,
        "json": case["json"] if case["json"] else None,
        "files": case["files"] if case["files"] else None,
        "headers": case["headers"] if case["headers"] else None,
    }
    logging.info(f"请求数据: {request_data}")
    allure.attach(json.dumps(request_data), name="请求数据")
    return request_data


@allure.step("发送HTTP请求")
def send_http_request(**request_data):
    """
    发送HTTP请求
    :param request_data: 请求数据
    :return: 响应数据
    """
    response = requests.request(**request_data)
    logging.info(f"响应数据: {response.text}")
    return response


@allure.step("发送JDBC请求")
def send_jdbc_request(sql, n=0):
    """
    发送JDBC请求
    :param sql: SQL语句
    :param n: 第n条数据
    :return: 响应数据
    """
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        charset="utf8mb4",
        autocommit=True
    )

    try:
        with conn.cursor() as cursor:
            affected = cursor.execute(sql)
            logging.info(f"影响 {affected} 条数据")

            sql_upper = sql.strip().upper()
            if sql_upper.startswith("SELECT"):
                result = cursor.fetchone()
                if result:
                    logging.info(f"查询结果: {result[n]}")
                    return result[n]
            else:
                logging.info(f"非查询语句，影响行数: {affected}")
    finally:
        conn.close()


@allure.step("http断言")
def http_assert(case, response):
    """
    http断言
    :param case: 测试用例
    :param response: 响应数据
    :return:
    """
    # 1. 检查响应状态码，非2xx直接失败并打印响应体
    if response.status_code >= 400:
        msg = f"请求失败，状态码：{response.status_code}，响应体：{response.text}"
        logging.error(msg)
        raise AssertionError(msg)

    if case["check"]:
        # 2. 尝试解析JSON
        try:
            resp_json = response.json()
        except json.JSONDecodeError as e:
            msg = f"响应不是有效的JSON，无法解析：{e}，响应体：{response.text}"
            logging.error(msg)
            raise AssertionError(msg)

        # 3. 执行jsonpath提取
        match_list = jsonpath.jsonpath(resp_json, case["check"])
        if not match_list:
            msg = (
                f"jsonpath表达式 '{case['check']}' 未匹配到任何结果\n"
                f"响应数据：{json.dumps(resp_json, ensure_ascii=False, indent=2)}"
            )
            logging.error(msg)
            raise AssertionError(msg)

        result = match_list[0]
        result_clean = str(result).strip()
        expect_clean = str(case['expect']).strip()
        logging.info(f"http断言实际结果：{result}==预期结果：{case['expect']}")
        assert result_clean == expect_clean
    else:
        logging.info(f"http断言实际结果：{response.text}包含预期结果：{case['expect']}")
        assert case["expect"] in response.text


def jdbc_assert(case):
    """
    jdbc断言
    :param case: 测试用例
    :return:
    """
    if case.get("sql_check") and case.get("sql_expected"):
        with allure.step("jdbc断言"):
            result = send_jdbc_request(case["sql_check"])
            expected = case["sql_expected"]
            result_str = str(result) if result is not None else "None"
            expect_str = str(expected) if expected is not None else "None"
            # 优先尝试数值比较：数据库Decimal可能带多余小数（如25.00），Excel中是int（25）
            try:
                if float(result_str) == float(expect_str):
                    logging.info(f"jdbc断言实际结果：{result_str}==预期结果：{expect_str}")
                    return
            except (ValueError, TypeError):
                pass
            logging.info(f"jdbc断言实际结果：{result_str}==预期结果：{expect_str}")
            assert result_str == expect_str
    elif case.get("sql_check"):
        with allure.step("执行sql"):
            send_jdbc_request(case["sql_check"])


def jdbc_extract(case, global_var):
    """
    jdbc提取
    :param case: 测试用例
    :param global_var: 全局变量
    :return:
    """
    if case.get("sqlExData"):
        with allure.step("jdbc提取"):
            for k, v in case["sqlExData"].items():
                global_var[k] = send_jdbc_request(v)
    logging.info(f"jdbc提取变量:{global_var}")


def json_extract(case, global_var, response):
    """
    json提取
    :param case: 测试用例
    :param global_var: 全局变量
    :param response: 响应数据
    :return:
    """
    if case.get("jsonExData"):
        with allure.step("json提取"):
            for k, v in case["jsonExData"].items():
                if k in global_var:
                    logging.info(f"跳过提取：{k} 已存在 (={global_var[k]})")
                    continue
                value = jsonpath.jsonpath(response.json(), v)
                if value:
                    global_var[k] = value[0]
    logging.info(f"json提取变量:{global_var}")