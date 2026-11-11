import allure


def allure_init(case):
    """
    初始化Allure报告
    """
    allure.dynamic.feature(case["feature"])
    allure.dynamic.story(case["story"])
    allure.dynamic.title(case["title"])
