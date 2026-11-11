from base.base import BasePage
from locators_helper import *
from locators_helper import _x


class StockLink(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 新建入库单

        self.add_stock_in_btn = btn_by_text("新建商品入库单")
        self.input_stock_in_num = input_by_label("入库单号")
        self.select_stock_in_repo = select_by_placeholder("请选择入库仓库")
        self.input_stock_in_repo_filter = select_input("请选择入库仓库")
        self.select_stock_in_type = select_by_placeholder("入库类型")
        self.input_stock_in_type_filter = select_input("入库类型")
        self.btn_add_stock_in = btn_by_text("添加")
        self.input_goods_search = _x(
            '(//tr[contains(@class,"el-table__row")])[1]//input[contains(@class,"el-select__input")]')  # 商品sku搜索
        self.input_goods_num = table_cell_input(1, "请输入商品数量")  # 明细表第1行的数量输入框
        self.input_operator = input_by_placeholder("请输入操作人")
        self.btn_create_stock_ordering = btn_by_text("创建入库单")
        self.create_stock_in_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"创建成功")]]')
        self.btn_create_stock_ordering = btn_by_text("创建入库单")
        # 执行入库
        self.btn_stock_in_row = row_btn("RK20260929001", "入库")
        # 弹窗内第1行的入库数量输入框
        self.input_stock_into_num = _x(f'{dialog("入库操作")}//input[@placeholder="入库数量"]')
        # 弹窗内第1行的入库绿色按钮（弹窗内明细只有一行，无需行号限定）
        self.btn_confirm_stock_in = _x(
            f'{dialog("入库操作")}//tr[contains(@class,"el-table__row")]//button[contains(@class,"el-button--success")]')
        self.confirm_stock_in_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"入库成功")]]')
        # 入库成功后点❌
        self.btn_close_stock_in_dialog = dialog_close(title="入库操作")

        # 新建出库单
        self.add_stock_out_btn = btn_by_text("新建商品出库单")
        self.input_stock_out_num = input_by_label("出库单号")
        self.select_stock_out_repo = select_by_placeholder("请选择出库仓库")
        self.input_stock_out_repo_filter = select_input("请选择出库仓库")
        self.select_stock_out_type = select_by_placeholder("出库类型")
        self.input_stock_out_type_filter = select_input("出库类型")
        self.btn_add_stock_out = btn_by_text("添加")
        self.input_goods_out_search = _x(
            '(//tr[contains(@class,"el-table__row")])[1]//input[contains(@class,"el-select__input")]')  # 商品sku搜索
        self.input_goods_out_num = table_cell_input(1, "请输入数量")  # 出库页明细数量框placeholder与入库页不同
        self.btn_create_stock_out_ordering = btn_by_text("创建出库单")
        self.create_stock_out_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"创建成功")]]')
        # 执行出库
        self.btn_stock_out_row = row_btn("CK20260929001", "出库")
        self.btn_confirm_stock_out = btn_by_text("确认出库")
        self.confirm_stock_out_success = _x('//div[contains(@class,"el-message")][.//*[contains(.,"出库成功")]]')
        self.btn_back_stock_out = btn_by_text("返回")

    def select_sku_goods(self, sku):
        """行内搜索商品SKU并选中联想项
        :param sku: 搜索关键词，如 SKU编码 CATE-UITEST-001-C-001
        """
        self.base_click(self.input_goods_search)  # 点开下拉
        self.fd_element(self.input_goods_search).send_keys(sku)  # 输入触发远程搜索
        self.base_click(select_option(sku))  # 等联想项出现并点中

    def create_stock_in(self, StockInNo, storage, storageType, sku, operator, goodsNum, StockInNum):
        """新建商品入库单
        :param StockInNo: 入库单号
        :param storage: 入库仓库
        :param storageType: 入库类型
        :param sku: 商品SKU
        :param operator: 操作人
        :param goodsNum: 商品数量
        :param StockInNum: 入库数量
        """
        open_menu(self, "仓库管理", "入库管理")
        self.base_click(self.add_stock_in_btn)
        self.base_clear(self.input_stock_in_num, StockInNo)
        select_el(self, "请选择入库仓库", storage)
        self.base_click(self.select_stock_in_type)
        self.base_click(select_option(storageType))
        self.base_click(self.btn_add_stock_in)
        self.select_sku_goods(sku)
        self.base_clear(self.input_goods_num, goodsNum)
        self.base_input(self.input_operator, operator)
        self.base_click(self.btn_create_stock_ordering)
        # 点开入库操作弹窗
        self.base_click(self.btn_stock_in_row)
        self.base_input(self.input_stock_into_num, StockInNum)
        self.base_click(self.btn_confirm_stock_in)
        # 关闭入库操作弹窗，释放遮罩
        self.base_click(self.btn_close_stock_in_dialog)

    def create_stock_out(self, StockOutNo, outType, storage, sku, goodsNum):
        """新建商品出库单
        :param StockOutNo: 出库单号
        :param outType: 出库类型
        :param storage: 出库仓库
        :param sku: 商品SKU
        :param goodsNum: 商品数量
        """
        open_menu(self, "仓库管理", "出库管理")
        self.base_click(self.add_stock_out_btn)
        self.base_clear(self.input_stock_out_num, StockOutNo)
        self.base_click(self.select_stock_out_type)
        self.base_click(select_option(outType))
        select_el(self, "请选择出库仓库", storage)
        self.base_click(self.btn_add_stock_out)
        self.select_sku_goods(sku)
        self.base_clear(self.input_goods_out_num, goodsNum)
        self.base_click(self.btn_create_stock_out_ordering)
        # 点开出库操作弹窗
        self.base_click(self.btn_stock_out_row)
        self.base_click(self.btn_confirm_stock_out)
        self.base_click(self.btn_back_stock_out)
