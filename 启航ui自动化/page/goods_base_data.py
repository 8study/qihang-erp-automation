from locators_helper import *

from base.base import BasePage


class GoodsBaseData(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        #  新增分类
        self.menu_goods = sub_menu("商品管理")  # 父菜单，先点展开
        self.menu_category = menu_item("商品分类管理")  # 新增分类/规格属性
        self.btn_category_add = btn_by_text("新增")  # 页面头部新增按钮
        self.input_category_num = input_in_dialog("添加商品分类", "请输入分类编码")
        self.input_category_name = input_in_dialog("添加商品分类", "请输入分类名称")
        self.input_category_remark = textarea_in_dialog("添加商品分类", "请输入备注")  # 备注是 textarea
        self.input_category_sort = input_in_dialog("添加商品分类", "请输入排序值")
        self.btn_dialog_confirm = btn_in_dialog("添加商品分类", "确 定")
        self.success_result = table_row("UI测试分类")

        #  新增规格属性
        self.btn_category_spec = row_btn("UI测试分类", "规格属性")  # 分类行内"规格属性"按钮，点击进入属性页
        self.btn_attr_add = btn_by_text("新增")  # 属性页头部新增按钮
        self.input_attr_title = input_in_dialog("添加属性", "请输入属性名")
        self.input_attr_sort = input_in_dialog("添加属性", "请输入排序")
        self.btn_attr_confirm = btn_in_dialog("添加属性", "确 定")

        #  新增属性值
        self.btn_attr_value = row_btn("颜色", "属性值管理")  # 属性"颜色"行内"属性值管理"，点击进入属性值页
        self.btn_value_add = btn_by_text("新增")  # 属性值页头部新增
        self.input_value = input_in_dialog("添加属性值", "请输入属性值")
        self.input_value_sort = input_in_dialog("添加属性值", "请输入排序")
        self.btn_value_confirm = btn_in_dialog("添加属性值", "确 定")

        #  新增品牌
        self.menu_brand = menu_item("商品品牌管理")  # 侧边栏品牌管理入口
        self.btn_brand_add = btn_by_text("新增")  # 品牌页头部新增
        self.input_brand_name = input_in_dialog("添加商品品牌", "请输入品牌名")
        self.input_brand_num = input_in_dialog("添加商品品牌", "请输入品牌编码")
        self.btn_brand_confirm = btn_in_dialog("添加商品品牌", "确 定")

        #  添加商品（含SKU）
        self.menu_goods_lib = menu_item("商品库管理")  # 侧边栏商品库入口
        self.btn_goods_add = btn_by_text("添加商品")  # 商品库列表页头部"添加商品"按钮
        # 商品分类（Treeselect 组件本质是 filterable el-select）
        self.select_category = select_by_placeholder("请选择上级菜单")
        self.input_category_filter = select_input("请选择上级菜单")
        # 品牌 / 供应商（filterable el-select）
        self.select_brand = select_by_placeholder("请选择品牌")
        self.input_brand_filter = select_input("请选择品牌")
        self.select_supplier = select_by_placeholder("请选择供应商")
        self.input_supplier_filter = select_input("请选择供应商")
        # 商品名称 / 商品编号（编号由"生成商品编码"按钮自动填充）
        self.input_goods_name = input_by_placeholder("请输入商品名称")
        self.input_goods_num = input_by_placeholder("请输入商品编号")
        self.btn_gen_goods_num = btn_by_text("生成商品编码")
        # 规格1（颜色列）multiple + filterable + allow-create：输入值回车创建
        self.select_color_spec = select_by_placeholder("自定义规格（可以上传图片）")
        self.input_color_spec = select_input("自定义规格（可以上传图片）")
        # 页面底部提交按钮（进入添加商品页后页面上唯一的"添加商品"按钮）
        self.btn_submit_goods = btn_by_text("添加商品")
        # 商品库列表断言
        self.success_result = table_row("UI测试商品")

    def click_operate(self):
        """点击操作"""
        self.base_click(self.menu_goods)
        self.base_click(self.menu_category)
        self.base_click(self.btn_category_add)

    def input_context(self, categoryNum, categoryName, remark, sort):
        """输入内容
        :param categoryNum: 分类编码
        :param categoryName: 分类名称
        :param remark: 备注
        :param sort: 分类排序
        """
        self.base_input(self.input_category_num, categoryNum)
        self.base_input(self.input_category_name, categoryName)
        self.base_input(self.input_category_remark, remark)
        self.base_input(self.input_category_sort, sort)

    def click_confirm(self):
        """点击确认"""
        self.base_click(self.btn_dialog_confirm)

    def add_goods_category(self, categoryNum, categoryName, remark, sort):
        """添加商品分类
        :param categoryNum: 分类编码
        :param categoryName: 分类名称
        :param remark: 备注
        :param sort: 分类排序
        """
        self.click_operate()
        self.input_context(categoryNum, categoryName, remark, sort)
        self.click_confirm()

    def add_goods_attribute(self, title, sort):
        """添加商品规格属性
        :param title: 属性名
        :param sort: 属性排序
        """
        # 分类列表页点"UI测试分类"行内"规格属性"进入属性页 → 点新增 → 填表 → 确定
        self.base_click(self.btn_category_spec)
        self.base_click(self.btn_attr_add)
        self.base_input(self.input_attr_title, title)
        self.base_input(self.input_attr_sort, sort)
        self.base_click(self.btn_attr_confirm)

    def enter_attribute_value(self):
        """进入属性值页"""
        self.base_click(self.btn_attr_value)

    def add_attribute_value(self, value, sort):
        """添加商品规格属性值
        :param value: 属性值
        :param sort: 属性值排序
        """
        self.base_click(self.btn_value_add)
        self.base_input(self.input_value, value)
        self.base_input(self.input_value_sort, sort)
        self.base_click(self.btn_value_confirm)

    def add_brand(self, name, num):
        """添加商品品牌
        :param name: 品牌名称
        :param num: 品牌编码
        """
        # 当前在属性值页，点左侧"商品品牌管理"进入品牌页 → 点新增 → 填表 → 确定
        self.base_click(self.menu_brand)
        self.base_click(self.btn_brand_add)
        self.base_input(self.input_brand_name, name)
        self.base_input(self.input_brand_num, num)
        self.base_click(self.btn_brand_confirm)

    def add_goods(self, category, brand, supplier, name, spec_values, pur_price, retail_price):
        """添加商品（含SKU）
        :param category: 商品分类名称，如"UI测试分类"
        :param brand: 品牌名称，如"测试品牌B"
        :param supplier: 供应商名称，如"Ikun练习供应商"
        :param name: 商品名称，如"UI测试商品"
        :param spec_values: 规格值列表（规格1输入值回车创建，生成几个值就有几行SKU），如 ["红M", "蓝L"]
        :param pur_price: 每个SKU的采购价
        :param retail_price: 每个SKU的零售价
        """
        # 1. 左侧栏"商品库管理" → 头部"添加商品"按钮进入添加商品页
        self.base_click(self.menu_goods_lib)
        self.base_click(self.btn_goods_add)
        # 2. 商品分类（下拉过滤选择"UI测试分类"）
        select_el(self, "请选择上级菜单", category)
        # 3. 填商品名称（生成商品编码前必须）
        self.base_input(self.input_goods_name, name)
        # 4. 点"生成商品编码"（需先选分类+填名称，自动填充商品编号）
        self.base_click(self.btn_gen_goods_num)
        # 5. 品牌
        select_el(self, "请选择品牌", brand)
        # 6. 供应商
        select_el(self, "请选择供应商", supplier)
        # 7. 规格1（颜色列）输入规格值回车创建（allow-create）
        select_multiple_create(self, "自定义规格（可以上传图片）", spec_values)
        # 8. SKU 表按行填采购价/零售价/单位（行数 = 规格值个数）
        for i in range(1, len(spec_values) + 1):
            sku_cell_input(self, i, "采购价", pur_price)
            sku_cell_input(self, i, "零售价", retail_price)
            sku_cell_input(self, i, "单位", "件")
        # 9. 提交
        self.base_click(self.btn_submit_goods)


    def del_goods(self, goods_name):
        """删除商品库商品（先进入商品库管理页 → 行内删除 + 确认弹窗）
        数据不存在时跳过，避免清理报超时
        :param goods_name: 商品名称，如"UI测试商品"
        """
        open_menu(self, "商品管理", "商品库管理")
        if not is_visible(self, row_btn(goods_name, "删除")):
            return
        self.base_click(row_btn(goods_name, "删除"))
        self.base_click(msgbox_btn("确定"))

    def del_brand(self, brand_name):
        """删除商品品牌（先进入品牌管理页 → 行内删除 + 确认弹窗）
        数据不存在时跳过，避免清理报超时
        :param brand_name: 品牌名称，如"测试品牌B"
        """
        open_menu(self, "商品管理", "商品品牌管理")
        if not is_visible(self, row_btn(brand_name, "删除")):
            return
        self.base_click(row_btn(brand_name, "删除"))
        self.base_click(msgbox_btn("确定"))

    def del_category(self, category_name):
        """删除商品分类（先进入分类管理页 → 树形表格行内删除 + 确认弹窗）
        数据不存在时跳过，避免清理报超时
        :param category_name: 分类名称，如"UI测试分类"
        """
        open_menu(self, "商品管理", "商品分类管理")
        if not is_visible(self, row_btn(category_name, "删除")):
            return
        self.base_click(row_btn(category_name, "删除"))
        self.base_click(msgbox_btn("确定"))

    def cleanup_data(self):
        """S2 数据清理：依次删除 商品 → 品牌 → 分类（顺序不可颠倒，先释放引用再删主数据）"""
        self.del_goods("UI测试商品")
        self.del_brand("测试品牌B")
        self.del_category("UI测试分类")
