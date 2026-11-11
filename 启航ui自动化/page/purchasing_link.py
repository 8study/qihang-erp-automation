from base.base import BasePage
from locators_helper import *
from locators_helper import _x


class PurchasingLinkPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 创建快递公司
        self.menu_purchase = sub_menu("采购管理")
        self.menu_purchase_supplier = menu_item("采购承运商")
        self.add_purchase_supplier_btn = btn_by_text("新增")
        self.input_express_company = input_in_dialog("添加快递公司", "请输入快递公司名称")
        self.input_express_company_code = input_in_dialog("添加快递公司", "请输入快递公司编码")
        self.input_company_description = textarea_in_dialog("添加快递公司", "请输入描述")
        self.btn_company_confirm = btn_in_dialog("添加快递公司", "确 定")
        self.create_purchase_supplier_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"新增成功")]]')

        # 创建采购单
        self.menu_purchase_order = menu_item("采购订单")
        self.add_purchase_order_btn = btn_by_text("创建采购订单")
        self.select_supplier = select_by_placeholder("请选择供应商名称")
        self.input_supplier_filter = select_input("请选择供应商名称")
        self.add_purchase_goods_btn = btn_by_text("添加商品")
        self.input_sku = input_in_dialog("选择商品", "请输入SKU编码")
        self.purchase_search_btn = btn_by_text("搜索")
        # 勾选订单
        self.chk_order_row = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"CATE-UITEST-001-C-001")]]'
            '//td[1]//label[contains(@class,"el-checkbox")]')
        self.purchase_confirm_btn = btn_by_text("确认添加")
        self.input_purchase_num = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"CATE-UITEST-001-C-001")]]'
            '//input[@placeholder="请输入数量"]')
        self.btn_create_order = btn_by_text("立即创建")
        self.create_purchase_order_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"新增成功")]]')

        # 审核
        self.purchase_audit_btn = btn_by_text("审核")
        self.input_purchase_assessor = input_in_dialog("审核采购订单", "请输入采购单审核人")
        self.btn_audit_confirm = btn_in_dialog("审核采购订单", "确 定")
        self.tag_order_audited = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"Ikun练习供应商")]]'
            '//td[8]//span[contains(@class,"el-tag")][normalize-space()="已审核"]')

        # 供应商发货
        self.assessor_delivery_btn = btn_by_text("供应商发货")
        self.select_express_company = select_by_placeholder("选择快递公司")
        self.input_express_company_filter = select_input("选择快递公司")
        self.input_logpress_no = input_in_dialog("供应商发货", "请输入物流单号")
        self.input_logpress_freight = input_in_dialog("供应商发货", "请输入物流费用")
        self.btn_logpress_confirm = btn_in_dialog("供应商发货", "确 定")
        self.tag_order_shipped = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"Ikun练习供应商")]]'
            '//td[8]//span[contains(@class,"el-tag")][normalize-space()="供应商已发货"]')

        # 收货
        self.menu_purchase_stock_in = menu_item("采购入库")
        self.receipt_btn = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"SF9876543210")]]'
            '//button[.//span[normalize-space()="收货"]]')
        self.btn_receipt_confirm = btn_in_dialog("确认收货", "确 定")
        self.tag_order_received = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"SF9876543210")]]'
            '//td[10]//span[contains(@class,"el-tag")][normalize-space()="已收货"]')

        # 生成入库单
        self.stock_in_btn = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"SF9876543210")]]'
            '//button[.//span[normalize-space()="入库"]]')
        self.select_stock_in_warehouse = select_by_placeholder("请选择入库仓库")
        self.input_stock_in_warehouse_filter = select_input("请选择入库仓库")
        self.btn_create_purchase_stock_in = btn_by_text("生成采购入库单")
        self.tag_order_stock_in_success = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"SF9876543210")]]'
            '//td[10]//span[contains(@class,"el-tag")][normalize-space()="已入库"]')


    def enter_add_purchase_supplier(self):
        """
        进入手动添加采购承运商页面
        """
        self.base_click(self.menu_purchase)
        self.base_click(self.menu_purchase_supplier)
        self.base_click(self.add_purchase_supplier_btn)

    def add_purchase_supplier(self, express_company, express_company_code, company_description):
        """
        添加采购承运商
        :param express_company: 快递公司名称
        :param express_company_code: 快递公司编码
        :param company_description: 描述
        """
        self.enter_add_purchase_supplier()
        self.base_input(self.input_express_company, express_company)
        self.base_input(self.input_express_company_code, express_company_code)
        self.base_input(self.input_company_description, company_description)
        self.base_click(self.btn_company_confirm)

    def enter_create_purchase_order(self):
        """
        进入手动创建采购订单页面
        """
        self.base_click(self.menu_purchase_order)
        self.base_click(self.add_purchase_order_btn)

    def create_purchase_order(self, supplier, sku, purchase_num):
        """
        创建采购订单
        :param supplier: 供应商名称
        :param sku: 商品SKU
        :param purchase_num: 采购数量
        """
        self.enter_create_purchase_order()
        select_el(self, "请选择供应商名称", supplier)
        self.base_click(self.add_purchase_goods_btn)
        self.base_input(self.input_sku, sku)
        self.base_click(self.purchase_search_btn)
        self.base_click(self.chk_order_row)
        self.base_click(self.purchase_confirm_btn)
        self.base_clear(self.input_purchase_num, purchase_num)
        self.base_click(self.btn_create_order)

    def purchase_audit(self, assessor):
        """
        审核采购订单
        :param assessor: 采购单审核人
        """
        self.base_click(self.purchase_audit_btn)
        self.base_input(self.input_purchase_assessor, assessor)
        self.base_click(self.btn_audit_confirm)

    def supplier_deliver(self, company,logpressNo,freight):
        """
        供应商发货
        :param company: 快递公司名称
        :param logpressNo: 物流单号
        :param freight: 物流费用
        """
        self.base_click(self.assessor_delivery_btn)
        select_el(self,"选择快递公司",company)
        self.base_input(self.input_logpress_no,logpressNo)
        self.base_clear(self.input_logpress_freight,freight)
        self.base_click(self.btn_logpress_confirm)

    def receive_purchase(self):
        """
        收货采购订单
        """
        self.base_click(self.menu_purchase_stock_in)
        self.base_click(self.receipt_btn)
        self.base_click(self.btn_receipt_confirm)

    def stock_in_purchase(self, warehouse):
        """
        生成采购入库单
        :param warehouse: 入库仓库
        """
        self.base_click(self.menu_purchase_stock_in)
        # 行内"入库"按钮（仅已收货状态显示），点击后跳转入库单生成页，仓库下拉框在那页上
        self.base_click(self.stock_in_btn)
        select_el(self, "请选择入库仓库", warehouse)
        self.base_click(self.btn_create_purchase_stock_in)

