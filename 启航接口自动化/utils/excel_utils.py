import json
import logging

import openpyxl

from config import EXCEL_NAME, SHEET_NAME
import os


def read_excel(filename=EXCEL_NAME, sheet_name=SHEET_NAME, feature=None):
    """
    读取Excel文件中的数据

    :param filename: Excel文件名
    :param sheet_name: 工作表名称
    :param feature: 按 feature 字段过滤（如 "登录"、"商品分类"），为 None 时返回所有模块
    :return: 数据列表
    """
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(project_dir, "data", filename)

    wb = openpyxl.load_workbook(excel_path)
    ws = wb[sheet_name]

    data = []

    keys = [cell.value for cell in ws[2]]

    for row in ws.iter_rows(min_row=3, values_only=True):
        if row[0] is None:
            continue
        case = dict(zip(keys, row))
        for field in ("params", "data", "json", "files", "headers", "sqlExData", "jsonExData"):
            if case.get(field) and isinstance(case[field], str):
                try:
                    case[field] = json.loads(case[field])
                except (json.JSONDecodeError, TypeError):
                    logging.info(f"字段{field}不是json格式，无需解析")
        if case.get("is_true"):
            if feature is None or case.get("feature") == feature:
                data.append(case)
    wb.close()
    return data


if __name__ == '__main__':
    print(read_excel())