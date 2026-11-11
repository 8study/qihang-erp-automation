"""
角色-用户-RBAC 链路页面对象
流程：新增角色（菜单权限仅勾选"商品管理"）→ 新增用户（关联该角色）→ 新账号登录验证菜单权限
"""
from base.base import BasePage
from locators_helper import *
from locators_helper import _x
from page.page_login import PageLogin


class RoleUserLinkPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # ---------- 新增角色 ----------
        self.add_role_btn = btn_by_text("新增")
        # 角色名称/权限字符在顶部搜索栏与弹窗内各有一份（placeholder 同名），必须锁弹窗
        self.input_role_name = input_in_dialog("添加角色", "请输入角色名称")
        self.input_role_key = input_in_dialog("添加角色", "请输入权限字符")
        # 角色顺序是 el-input-number，没有 placeholder，按表单项 label 定位
        self.input_role_sort = input_by_label("角色顺序")
        # 状态单选框（字典 sys_normal_disable：0=正常/启用，1=停用），默认已是"正常"
        self.radio_role_normal = _x(
            dialog("添加角色") + '//label[contains(@class,"el-radio")]'
            '[.//span[contains(@class,"el-radio__label")][normalize-space()="正常"]]')
        # 菜单权限树：只勾"商品管理"顶层节点——父子联动默认开启（menuCheckStrictly=true），
        # 勾父节点会连带选中其下全部子菜单，正好满足"仅勾选商品管理相关菜单"
        self.tree_menu_goods = _x(
            dialog("添加角色") +
            '//div[contains(@class,"el-tree-node__content")]'
            '[.//span[contains(@class,"el-tree-node__label")][normalize-space()="商品管理"]]'
            '//span[contains(@class,"el-checkbox__inner")]')
        self.input_role_remark = textarea_in_dialog("添加角色", "请输入内容")
        self.btn_role_confirm = btn_in_dialog("添加角色", "确 定")
        self.create_role_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"新增成功")]]')

        # ---------- 新增用户 ----------
        self.add_user_btn = btn_by_text("新增")
        self.input_nick_name = input_in_dialog("添加用户", "请输入用户昵称")
        # 手机号码/用户名称同样与搜索栏 placeholder 重名，必须锁弹窗
        self.input_phone = input_in_dialog("添加用户", "请输入手机号码")
        self.input_email = input_in_dialog("添加用户", "请输入邮箱")
        self.input_user_name = input_in_dialog("添加用户", "请输入用户名称")
        self.input_user_password = input_in_dialog("添加用户", "请输入用户密码")
        self.radio_user_normal = _x(
            dialog("添加用户") + '//label[contains(@class,"el-radio")]'
            '[.//span[contains(@class,"el-radio__label")][normalize-space()="正常"]]')
        self.input_user_remark = textarea_in_dialog("添加用户", "请输入内容")
        self.btn_user_confirm = btn_in_dialog("添加用户", "确 定")
        self.create_user_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"新增成功")]]')
        # 多选下拉选完不会自动收起，会挡住下方备注和确定按钮，需要点外部让面板关闭
        self.dialog_user_title = _x(dialog("添加用户") + '//span[contains(@class,"el-dialog__title")]')

        # ---------- 登录后侧边栏（RBAC 断言用） ----------
        self.sidebar_goods = sub_menu("商品管理")

    def add_role(self, role_name, role_key, role_sort, remark):
        """
        新增角色，菜单权限仅勾选"商品管理"（父节点联动其下全部子菜单）
        :param role_name: 角色名称
        :param role_key: 权限字符
        :param role_sort: 角色顺序
        :param remark: 备注
        """
        open_menu(self, "系统设置", "角色管理")
        self.base_click(self.add_role_btn)
        self.base_input(self.input_role_name, role_name)
        self.base_input(self.input_role_key, role_key)
        self.base_input(self.input_role_sort, role_sort)
        self.base_click(self.radio_role_normal)  # 状态=正常（启用）
        self.base_click(self.tree_menu_goods)    # 只勾商品管理
        self.base_input(self.input_role_remark, remark)
        self.base_click(self.btn_role_confirm)

    def add_user(self, nick_name, phone, email, user_name, password, sex, role_name, remark):
        """
        新增用户并关联指定角色
        :param nick_name: 用户昵称
        :param phone: 手机号码
        :param email: 邮箱
        :param user_name: 用户名称（登录账号）
        :param password: 用户密码
        :param sex: 用户性别（男/女/未知）
        :param role_name: 关联角色名称
        :param remark: 备注
        """
        open_menu(self, "系统设置", "用户管理")
        self.base_click(self.add_user_btn)
        self.base_input(self.input_nick_name, nick_name)
        self.base_input(self.input_phone, phone)
        self.base_input(self.input_email, email)
        self.base_input(self.input_user_name, user_name)
        self.base_input(self.input_user_password, password)
        select_in_dialog(self, "添加用户", "请选择性别", sex)
        self.base_click(self.radio_user_normal)  # 状态=正常（启用）
        select_in_dialog(self, "添加用户", "请选择角色", role_name)
        # 角色是多选下拉，选中后面板不收起，先点弹窗标题触发"点击外部"关闭面板，
        # 否则面板会盖住下面的备注框和确定按钮导致点击被拦截
        self.base_click(self.dialog_user_title)
        self.base_input(self.input_user_remark, remark)
        self.base_click(self.btn_user_confirm)

    def relogin(self, user_name, password):
        """
        退出当前账号后以新账号登录（token 存在 Cookie Admin-Token 里，清 Cookie 即退出），
        用于验证新用户的 RBAC 菜单权限
        :param user_name: 登录账号
        :param password: 登录密码
        """
        self.driver.delete_all_cookies()
        page_login = PageLogin(self.driver)
        page_login.get_url()
        page_login.login(user_name, password)
