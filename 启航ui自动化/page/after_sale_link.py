from base.base import BasePage
from locators_helper import *
from locators_helper import _x


class AfterSaleLinkPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 添加售后
        self.menu_orders = sub_menu("订单管理")
        self.menu_after_sale_ledger = menu_item("售后台账")
        self.add_after_sale_btn = btn_by_text("手动添加")
        self.select_after_sale_type = select_by_placeholder("请选择类型")
        self.input_after_sale_filter = select_input("请选择类型")
        self.input_after_sale_no = input_in_dialog("手动添加售后记录", "请输入售后单号")
        self.input_order_no = input_in_dialog("手动添加售后记录", "请输入订单号")
        self.input_product_name = input_in_dialog("手动添加售后记录", "请输入商品名称")
        self.input_sku_code = input_in_dialog("手动添加售后记录", "请输入Sku编码")
        self.input_quantity = input_in_dialog("手动添加售后记录", "请输入数量")
        self.input_remark = input_in_dialog("手动添加售后记录", "请输入备注")
        self.btn_after_sale_confirm = btn_in_dialog("手动添加售后记录", "确 定")
        self.create_after_sale_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"添加成功")]]')

        # 退货确认
        self.return_confirm_btn = _x(
            '//tr[contains(@class,"el-table__row")][.//td[contains(.,"CATE-UITEST-001-C-001")]]'
            '//button[.//span[normalize-space()="退货确认"]]')
        self.input_return_company_name = input_in_dialog("退货确认", "选择退回物流公司")
        self.input_return_company_filter = input_in_dialog("退货确认", "选择退回物流公司")
        self.input_return_no = input_in_dialog("退货确认", "请输入退回物流单号")
        # 备注是 type=textarea，渲染为 <textarea> 而非 <input>，要用 textarea_in_dialog
        self.input_return_remark = textarea_in_dialog("退货确认", "请输入备注")
        self.btn_return_confirm = btn_in_dialog("退货确认", "确 定")
        self.return_confirm_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"处理成功")]]')


    def enter_after_sale(self):
        """
        进入售后台账
        """
        self.base_click(self.menu_orders)
        self.base_click(self.menu_after_sale_ledger)
        self.base_click(self.add_after_sale_btn)

    def add_after_sale(self,type,AfterNo,OrderNo,ProductName,SkuCode,Quantity,Remark):
        """
        添加售后
        :param type: 售后类型
        :param AfterNo: 售后单号
        :param OrderNo: 订单号
        :param ProductName: 商品名称
        :param SkuCode: Sku编码
        :param Quantity: 数量
        :param Remark: 备注
        """
        self.enter_after_sale()
        select_in_dialog(self, "手动添加售后记录", "请选择类型", type)
        self.base_input(self.input_after_sale_no, AfterNo)
        self.base_input(self.input_order_no, OrderNo)
        self.base_input(self.input_product_name, ProductName)
        self.base_input(self.input_sku_code, SkuCode)
        self.base_input(self.input_quantity, Quantity)
        self.base_input(self.input_remark, Remark)
        self.base_click(self.btn_after_sale_confirm)

    def confirm_return(self,ReturnCompanyName,ReturnNo,Remark):
        """
        退货确认
        :param ReturnCompanyName: 退回物流公司
        :param ReturnNo: 退回物流单号
        :param Remark: 备注
        """
        self.base_click(self.return_confirm_btn)
        select_in_dialog(self,"退货确认","选择退回物流公司",ReturnCompanyName)
        self.base_input(self.input_return_no, ReturnNo)
        self.base_input(self.input_return_remark, Remark)
        self.base_click(self.btn_return_confirm)
