"""
页面元素定位辅助
================
把常用页面元素的定位方式集中在这里，页面样式调整时只改这一处即可。
包含两类函数：
  1) 定位器：只描述"元素在页面上的位置"，返回定位结果，交给页面基类去查找、点击、输入。
  2) 组件操作：立刻执行一次交互（下拉选择、表格填写等），第一个参数传页面基类实例。

用法：
    from locators_helper import input_by_placeholder, select_el
    self.input_name = input_by_placeholder("请输入商品名称")
    select_el(self, "请选择品牌", "测试品牌B")   # self 是页面基类实例
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def _x(xpath: str) -> tuple:
    """
    统一包装为 locator 元组
    :param xpath: xpath 表达式字符串
    :return: (By.XPATH, xpath) 元组
    """
    return (By.XPATH, xpath)


# ---------- 输入框：按框内提示文字定位最准确 ----------

def input_by_placeholder(placeholder: str) -> tuple:
    """
    定位页面或弹窗里的单行输入框，按框内提示文字匹配
    用来在输入框里填写内容，如填写"商品名称"
    :param placeholder: 输入框里的提示文字，如"请输入商品名称"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//input[@placeholder="{placeholder}"]')


def input_by_label(label: str) -> tuple:
    """
    定位没有提示文字的单行输入框，按它左侧的表单项名称匹配
    表单项说明文字在左侧、输入框在右侧时用这个
    :param label: 表单项名称，如"商品名称"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//div[contains(@class,"el-form-item")][.//label[contains(.,"{label}")]]//input')


# ---------- 按钮：按按钮上的文字定位 ----------

def btn_by_text(text: str) -> tuple:
    """
    定位页面上任意位置的按钮，按按钮文字匹配
    如搜索、重置、添加商品等
    :param text: 按钮文字，如"搜索"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//button[.//span[normalize-space()="{text}"]]')


# ---------- 表格：按"行内文字"或"行内按钮"定位 ----------

def table_row(row_text: str) -> tuple:
    """
    定位数据表格中包含指定内容的那一行
    用来确认某条数据已经出现在列表里，如断言"UI测试商品"出现
    :param row_text: 该行里唯一的内容，如商品编号
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//tr[contains(@class,"el-table__row")][.//td[contains(.,"{row_text}")]]')


def row_btn(row_text: str, btn_text: str) -> tuple:
    """
    定位表格某一行里的操作按钮，如编辑、删除、下架、查看明细
    :param row_text: 该行里唯一的内容，如商品编号
    :param btn_text: 按钮文字，如"编辑"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//tr[contains(@class,"el-table__row")][.//td[contains(.,"{row_text}")]]'
              f'//button[.//span[normalize-space()="{btn_text}"]]')


def table_cell_input(row_index: int, placeholder: str) -> tuple:
    """
    定位表格中第n行里的输入框
    用于在明细表格里按行填写，如添加商品时的采购价、零售价
    :param row_index: 行号，从 1 开始
    :param placeholder: 输入框里的提示文字，如"采购价"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'(//tr[contains(@class,"el-table__row")])[{row_index}]//input[@placeholder="{placeholder}"]')


# ---------- 下拉框 ----------
# 展开后的选项列表浮在页面最上层，和下拉框本身不在一起；
# 下拉框未选择时显示提示文字，选中后提示文字会消失，此时要按"当前正在输入的那个下拉框"定位。

def select_by_placeholder(placeholder: str) -> tuple:
    """
    定位页面上的下拉框，按框内提示文字匹配，点击它可展开选项列表
    :param placeholder: 下拉框里的提示文字，如"请选择品牌"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//div[contains(@class,"el-select")]'
              f'[.//div[contains(@class,"el-select__placeholder")][contains(.,"{placeholder}")]]')


def select_input(placeholder: str) -> tuple:
    """
    定位下拉框展开后出现的搜索输入框，按下拉框的提示文字匹配
    打开列表后用它输入文字筛选，或输入新值回车创建
    注意：选中选项后提示文字会消失，此定位不再有效，请改用 select_input_focused
    :param placeholder: 下拉框里的提示文字
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//div[contains(@class,"el-select")]'
              f'[.//div[contains(@class,"el-select__placeholder")][contains(.,"{placeholder}")]]'
              f'//input[contains(@class,"el-select__input")]')


def select_input_focused() -> tuple:
    """
    定位当前正在输入的那个下拉框的输入框，不依赖提示文字
    用于下拉框已选中部分内容、提示文字消失后继续输入，如规格"红M"回车生成规格
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//div[contains(@class,"el-select__wrapper")][contains(@class,"is-focused")]'
              f'//input[contains(@class,"el-select__input")]')


def select_option(option_text: str) -> tuple:
    """
    定位下拉框展开后的选项，按选项文字匹配
    页面上同时存在多个下拉框，此定位只锁定当前展开的那一个选项列表
    :param option_text: 选项文字，如"自营"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//div[contains(@class,"el-select__popper")][@aria-hidden="false"]'
              f'//li[contains(@class,"el-select-dropdown__item")][contains(.,"{option_text}")]')


# ---------- 弹窗：先锁定是哪个弹窗，再找弹窗里的元素 ----------

def dialog(title: str) -> str:
    """
    返回弹窗区域的定位片段，用来拼接弹窗内部元素（如弹窗里的输入框、按钮）
    :param title: 弹窗标题，如"添加商品"
    :return: 定位片段（不是完整定位结果），拼在内部元素定位前面使用
    """
    return (f'//div[contains(@class,"el-dialog")]'
            f'[.//span[contains(@class,"el-dialog__title")][contains(.,"{title}")]]')


def input_in_dialog(title: str, placeholder: str) -> tuple:
    """
    定位弹窗里的单行输入框，先锁定指定弹窗再找输入框
    避免和页面上提示文字相同的输入框混淆，如填写"分类编码"
    :param title: 弹窗标题
    :param placeholder: 输入框里的提示文字
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'{dialog(title)}//input[@placeholder="{placeholder}"]')


def textarea_in_dialog(title: str, placeholder: str) -> tuple:
    """
    定位弹窗里的多行文本框（可换行的大块文字输入区）
    :param title: 弹窗标题
    :param placeholder: 文本框里的提示文字
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'{dialog(title)}//textarea[@placeholder="{placeholder}"]')


def btn_in_dialog(title: str, text: str) -> tuple:
    """
    定位弹窗里的按钮，如"确 定"、"取 消"
    :param title: 弹窗标题
    :param text: 按钮文字
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'{dialog(title)}//button[.//span[normalize-space()="{text}"]]')


def msgbox_btn(text: str) -> tuple:
    """
    定位删除、下架等二次确认小窗口里的按钮
    :param text: 按钮文字，如"确定"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//div[contains(@class,"el-message-box")]//button[.//span[normalize-space()="{text}"]]')


def dialog_close(title: str = None, dialog_cls: str = None) -> tuple:
    """
    定位弹窗右上角的关闭按钮（×）
    :param title: 弹窗标题（与 dialog_cls 二选一，同时传时以 dialog_cls 为准）
    :param dialog_cls: 弹窗自带的自定义标记，如新手引导弹窗，最稳定
    :return: (By.XPATH, ...) 元组
    """
    if dialog_cls:
        scope = f'//div[contains(@class,"el-dialog")][contains(@class,"{dialog_cls}")]'
    elif title:
        scope = dialog(title)
    else:
        scope = '//div[contains(@class,"el-dialog")]'
    return _x(f'{scope}//button[contains(@class,"el-dialog__headerbtn")]')


# ---------- 标签页 / 左侧导航菜单 ----------

def tab_by_text(text: str) -> tuple:
    """
    定位内容区的切换标签页，如"按商品展示"、"按规格展示"
    :param text: 标签页文字
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//div[contains(@class,"el-tabs__item")][contains(.,"{text}")]')


def sub_menu(text: str) -> tuple:
    """
    定位左侧导航栏里可展开的菜单，点击后展开下级菜单
    :param text: 上级菜单文字，如"商品管理"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//li[contains(@class,"el-sub-menu")][.//span[normalize-space()="{text}"]]')


def menu_item(text: str) -> tuple:
    """
    定位左侧导航栏里的末级菜单，点击后跳转到对应页面
    :param text: 菜单文字，如"商品库管理"
    :return: (By.XPATH, ...) 元组
    """
    return _x(f'//li[contains(@class,"el-menu-item")][.//span[normalize-space()="{text}"]]')


# ---------- 组件操作：下拉选择 / 表格填写等整套动作（第一个参数传页面基类实例） ----------

def select_el(page, placeholder, value):
    """下拉框选择：点开下拉框 → 输入文字筛选 → 点中目标选项
    :param page: 页面基类实例
    :param placeholder: 下拉框提示文字，如"请选择品牌"
    :param value: 要选中的选项文字
    """
    # 点开下拉框，等选项列表显示出来
    page.base_click(select_by_placeholder(placeholder))
    # 输入文字筛选选项
    page.fd_element(select_input(placeholder)).send_keys(value)
    # 点中筛选后的选项
    page.base_click(select_option(value))


def select_in_dialog(page, title, placeholder, value):
    """弹窗里的下拉框选择：和页面搜索区提示文字相同的下拉框必须用这个，避免点错
    :param page: 页面基类实例
    :param title: 弹窗标题，如"手动添加售后记录"
    :param placeholder: 下拉框提示文字，如"请选择类型"
    :param value: 要选中的选项文字，如"退货"
    """
    # 点开弹窗里的下拉框（只在弹窗范围内查找）
    page.base_click(_x(
        dialog(title) +
        '//div[contains(@class,"el-select")]'
        f'[.//div[contains(@class,"el-select__placeholder")][contains(.,"{placeholder}")]]'))
    # 选项列表浮在页面上层，只锁定当前展开的那个，直接点选项
    # 不能输入文字筛选的下拉框没有搜索输入框，跳过筛选步骤
    page.base_click(select_option(value))


def select_multiple_create(page, placeholder, values):
    """批量新增规格：逐个输入内容并回车，每回车一次生成一个标签
    注意：选中第一个标签后提示文字会消失，后续输入要改用"当前正在输入的下拉框"定位。
    :param page: 页面基类实例
    :param placeholder: 下拉框提示文字（只在第一次打开时用）
    :param values: 要创建的规格值列表，如 ["红M", "蓝L"]
    """
    # 首次点开下拉框
    page.base_click(select_by_placeholder(placeholder))
    for v in values:
        # 输入规格值并回车生成标签
        inp = page.fd_element(select_input_focused())
        inp.send_keys(v)
        inp.send_keys(Keys.ENTER)
        # 等输入框清空后再输下一个，避免两个值拼在一起
        WebDriverWait(page.driver, page.timeout).until(
            lambda d: d.find_element(*select_input_focused()).get_attribute("value") == "")
    # 输完按 ESC 关闭下拉框
    try:
        page.fd_element(select_input_focused()).send_keys(Keys.ESCAPE)
    except Exception:
        pass


def sku_cell_input(page, row_index, placeholder, value):
    """在表格单元格里填写内容（采购价 / 零售价 / 单位等）
    这几列在表格最右侧、可能被屏幕边缘挡住，所以先等它出现，
    再滚动到视野内，最后填写。
    :param page: 页面基类实例
    :param row_index: 行号，从 1 开始
    :param placeholder: 输入框提示文字，如"采购价"
    :param value: 要填写的值
    """
    loc = table_cell_input(row_index, placeholder)
    # 只等元素出现（不要求可见，避免被挡住时误判）
    ele = WebDriverWait(page.driver, page.timeout).until(
        EC.presence_of_element_located(loc))
    # 滚动到视野内
    page.driver.execute_script(
        "arguments[0].scrollIntoView({block:'center',inline:'center'})", ele)
    ele.clear()
    ele.send_keys(value)


def is_visible(page, locator, timeout=3):
    """在短时间内判断元素是否显示出来（不存在或看不到都返回 False，不报错）
    判断期间临时关掉全局等待，否则找不到元素会被拖满 10 秒
    :param page: 页面基类实例
    :param locator: (By.XPATH, ...) 元组
    :param timeout: 最长等待秒数
    """
    page.driver.implicitly_wait(0)
    try:
        WebDriverWait(page.driver, timeout, poll_frequency=0.3).until(
            EC.visibility_of_element_located(locator))
        return True
    except Exception:
        return False
    finally:
        page.driver.implicitly_wait(10)


def open_menu(page, parent, child):
    """进入指定菜单页：下级菜单收起来时先展开上级菜单，再点击进入
    :param page: 页面基类实例
    :param parent: 上级菜单文字，如"商品管理"
    :param child: 末级菜单文字，如"商品库管理"
    """
    if not is_visible(page, menu_item(child)):
        page.base_click(sub_menu(parent))
    page.base_click(menu_item(child))
