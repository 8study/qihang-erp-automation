from base.base import BasePage
from config import *
from page.stock_link import StockLink
from script import log


class TestStockLink:

    def setup_method(self):
        # 前置清理：删掉上一轮创建的入库单 RK20260929001（子表 erp_stock_in_item 先删），
        # 保证用例可反复执行；页面无删除入口，只能走 SQL
        BasePage.sql_clean(STOCK_IN_SQLS, conn)
        log.info("前置SQL清理完成：已清空入库单 RK20260929001 及其明细")

    def teardown_method(self):
        # 只关闭本用例使用的连接；不清理数据，保留入库单供页面查看，
        # 重复执行由 setup_method 的前置清理保证
        conn.close()

    def test_create_stock_in(self, login_brower):
        try:
            page_stock_link = StockLink(login_brower)
            # 新建商品入库单
            page_stock_link.create_stock_in("RK20260929001", "华东主仓", "采购入库", "CATE-UITEST-001-C-001", "王维",
                                            "100", "40")
            result = page_stock_link.get_success_result(page_stock_link.confirm_stock_in_success)
            assert "入库成功" in result
            log.info(f"入库结果：{result}")
            page_stock_link.get_shot("confirm_stock_in_success.png")

            # 新建商品出库单
            page_stock_link.create_stock_out("CK20260929001", "订单发货出库", "华东主仓", "CATE-UITEST-001-C-001", "10")
            result = page_stock_link.get_success_result(page_stock_link.confirm_stock_out_success)
            assert "出库成功" in result
            log.info(f"出库结果：{result}")
            page_stock_link.get_shot("confirm_stock_out_success.png")

        except Exception as e:
            log.error(f"库存链路失败：{e}")
            StockLink(login_brower).get_shot("stock_link.png")
            raise e
