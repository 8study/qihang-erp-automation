from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from base.base import BasePage
from locators_helper import menu_item, btn_by_text, select_by_placeholder, select_input, input_by_placeholder, \
    input_by_label, table_cell_input, select_el, _x, sub_menu, dialog, dialog_close, msgbox_btn, row_btn, btn_in_dialog


class OrderingLink(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.menu_goods = sub_menu("商品管理")
        self.menu_shop_goods = menu_item("店铺商品管理")
        self.add_shop_goods_btn = btn_by_text("手动添加店铺商品")
        self.select_shop = select_by_placeholder("请选择店铺")
        self.input_shop_filter = select_input("请选择店铺")
        self.input_product_name = input_by_placeholder("请输入商品名称")
        self.input_product_code = input_by_placeholder("请输入商品编号，如 SP0001")
        self.input_product_id = input_by_placeholder("请输入平台商品ID（不填或填0则不校验唯一性）")
        self.input_price = input_by_label("商品价格")
        self.btn_add_sku_row = btn_by_text("添加规格行")
        # SKU名称
        self.input_sku_name = table_cell_input(1, "如 红色")
        # SKU编码
        self.input_sku_code = table_cell_input(1, "对应ERP商品SKU编码")

        self.input_sku_stock = (By.XPATH, '(//tr[contains(@class,"el-table__row")])[1]//td[4]//input')  # 库存
        self.input_sku_price = (By.XPATH, '(//tr[contains(@class,"el-table__row")])[1]//td[5]//input')  # 价格
        self.btn_save_sku = btn_by_text("保存")
        # 店铺商品保存成功提示
        self.shop_goods_save_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"保存成功")]]')

        # 手动添加店铺订单
        self.menu_orders = sub_menu("订单管理")
        self.menu_shop_orders = menu_item("店铺订单")
        self.add_shop_orders_btn = btn_by_text("手动添加店铺订单")
        self.input_order_no = input_by_placeholder("留空则自动生成订单号")
        self.order_select_shop = select_by_placeholder("启航淘宝旗舰店")
        self.input_order_filter = select_input("启航淘宝旗舰店")
        self.btn_add_goods = btn_by_text("添加商品")
        self.btn_add_target_goods = _x(
            f' {dialog("选择店铺商品")} ' f'//tr[contains(@class,"el-table__row")][.//td[contains(.,"UI测试店铺商品")]]' f'//button[.//span[normalize-space()="添加"]]')
        self.btn_close_dialog = dialog_close(title="选择店铺商品")  # 点击关闭弹窗
        self.input_receiver_name = input_by_placeholder("收件人姓名")
        self.input_receiver_phone = input_by_placeholder("收件人手机号")
        self.input_receiver_address = input_by_placeholder("详细地址（不含省市区）")

        # 地区选择
        self.cascader_region = input_by_placeholder("请选择省市区")
        self.input_freight = _x(f'//div[contains(@class,"summary-row")][.//span[normalize-space()="运费"]]//input')
        self.btn_submit_order = btn_by_text("提交订单")
        # 订单创建成功提示
        self.order_save_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"订单创建成功")]]')

        # 推送订单
        # 勾选订单
        self.chk_order_row = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"SO20260929001")]]'
            '//td[1]//label[contains(@class,"el-checkbox")]')
        # 推送按钮
        self.btn_push_orders = btn_by_text("重新推送选中订单到订单库")
        # ok按钮
        self.btn_confirm_push = msgbox_btn("OK")

        # 手动发货
        self.menu_delivery = sub_menu("发货管理")
        self.menu_hand_delivery = menu_item("手动发货")
        self.btn_hand_delivery = row_btn("SO20260929001", "手动发货")
        self.select_express_company = select_by_placeholder("选择快递公司")
        self.input_express_company_filter = select_input("选择快递公司")
        self.option_sf_taobao = _x(
            '//div[contains(@class,"el-select__popper")][@aria-hidden="false"]' '//li[contains(@class,"el-select-dropdown__item")]' '[contains(normalize-space(.),"顺丰速运")][contains(normalize-space(.),"淘宝天猫")]')
        self.input_express_no = input_by_placeholder("请输入物流单号")
        self.btn_submit_express = btn_in_dialog("打包发货", "确 定")
        self.hand_delivery_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"发货成功")]]')

    # 点开省市区的选项
    def cascader_node(self, text):
        return _x(
            f'//li[contains(@class,"el-cascader-node")]' f'[.//span[contains(@class,"el-cascader-node__label")][normalize-space()="{text}"]]')

    def enter_add_shop_goods(self):
        """
        进入手动添加店铺商品页面
        """
        self.base_click(self.menu_goods)
        self.base_click(self.menu_shop_goods)
        self.base_click(self.add_shop_goods_btn)

    def add_shop_goods(self, shop, product_name, product_code, product_id, sku_stock, sku_price):
        """
        添加店铺商品
        :param shop: 店铺名称
        :param product_name: 商品名称
        :param product_code: 商品编号
        :param product_id: 平台商品ID
        :param sku_stock: SKU库存
        :param sku_price: SKU价格
        """
        self.enter_add_shop_goods()
        # 选择店铺
        select_el(self, "请选择店铺", shop)
        # 输入商品名称
        self.base_input(self.input_product_name, product_name)
        # 输入商品编号
        self.base_input(self.input_product_code, product_code)
        # 输入平台商品ID
        self.base_input(self.input_product_id, product_id)
        # 输入商品价格
        self.base_clear(self.input_price, "20")
        # 点击添加规格行
        self.base_click(self.btn_add_sku_row)
        # 输入SKU名称
        self.base_input(self.input_sku_name, "红色")
        # 输入SKU编码
        self.base_input(self.input_sku_code, "CATE-UITEST-001-C-001")
        # 输入SKU库存
        self.base_clear(self.input_sku_stock, sku_stock)
        # 输入SKU价格
        self.base_clear(self.input_sku_price, sku_price)
        # 点击保存
        self.base_click(self.btn_save_sku)

    def enter_add_shop_orders(self):
        """
        进入手动添加店铺订单页面
        """
        self.base_click(self.menu_orders)
        self.base_click(self.menu_shop_orders)
        self.base_click(self.add_shop_orders_btn)

    def select_region(self, province, city, district):
        """选择省市区：点开面板 → 省 → 市 → 区（点中叶子自动收起）
        :param province: 省份
        :param city: 城市
        :param district: 区县
        """
        self.base_click(self.cascader_region)  # 点开面板
        for text in (province, city, district):  # 逐级点击
            self.base_click(self.cascader_node(text))

    def add_shop_orders(self,OrderNum,shop,name,phone,province,city,district,address,num):
        """
        添加店铺订单
        :param OrderNum: 订单号
        :param shop: 店铺名称
        :param name: 收货人姓名
        :param phone: 收货人手机号
        :param province: 省份
        :param city: 城市
        :param district: 区县
        :param address: 详细地址（不含省市区）
        :param num: 运费
        """
        self.enter_add_shop_orders()
        # 输入订单号
        self.base_input(self.input_order_no,OrderNum)
        # 选择店铺
        select_el(self, "启航淘宝旗舰店", shop)
        # 点击添加商品
        self.base_click(self.btn_add_goods)
        # 添加商品
        self.base_click(self.btn_add_target_goods)
        # 点击关闭弹窗
        self.base_click(self.btn_close_dialog)
        # 输入收货人姓名
        self.base_input(self.input_receiver_name,name)
        # 输入收货人手机号
        self.base_input(self.input_receiver_phone,phone)
        # 选择省市区
        self.select_region(province, city, district)
        # 输入详细地址（不含省市区）
        self.base_input(self.input_receiver_address, address)
        # 输入运费
        self.base_clear(self.input_freight, num)
        # 点击提交订单
        self.base_click(self.btn_submit_order)

    def push_orders(self):
        """
        推送订单
        """
        # 勾选订单
        self.base_click(self.chk_order_row)
        self.base_click(self.btn_push_orders)
        self.base_click(self.btn_confirm_push)

    def enter_hand_delivery(self):
        """
        进入手动发货页面
        """
        self.base_click(self.menu_delivery)
        self.base_click(self.menu_hand_delivery)
        self.base_click(self.btn_hand_delivery)

    def hand_delivery(self,express_no):
        """
        手动发货
        :param express_no: 物流单号
        """
        self.enter_hand_delivery()
        # 选择快递公司（带平台限定）
        self.base_click(self.select_express_company)  # select_by_placeholder("选择快递公司")
        self.fd_element(self.input_express_company_filter).send_keys("顺丰速运")  # select_input("选择快递公司")，触发过滤
        self.base_click(self.option_sf_taobao)
        # 输入物流单号
        self.base_input(self.input_express_no, express_no)
        # 点击提交
        self.base_click(self.btn_submit_express)


