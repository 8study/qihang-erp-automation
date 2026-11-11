from base.base import BasePage
from config import *
from page.purchasing_link import PurchasingLinkPage
from script import log


class TestPurchasingLink:

    def setup_method(self):
        # 前置清理：删掉上一轮创建的采购承运商和采购订单，保证用例可反复执行
        BasePage.sql_clean(PURCHASE_SUPPLIER_SQLS, conn)
        BasePage.sql_clean(PURCHASE_ORDER_SQLS, conn)
        log.info("前置SQL清理完成：已清空采购承运商 逆丰慢运（nf10086）及含测试SKU的采购订单")

    def teardown_method(self):
        conn.close()

    def test_add_purchasing_supplier(self, login_brower):
        try:
            # 添加快递公司
            purchasing_link_page = PurchasingLinkPage(login_brower)
            purchasing_link_page.add_purchase_supplier("逆丰慢运", "nf10086", "承诺，为每一份衬托")
            result = purchasing_link_page.get_success_result(purchasing_link_page.create_purchase_supplier_success)
            log.info(f"添加快递公司成功，结果：{result}")
            assert "新增成功" in result
            purchasing_link_page.get_shot("add_express_company_success.png")

            # 创建采购订单
            purchasing_link_page.create_purchase_order("Ikun练习供应商", "CATE-UITEST-001-C-001", "10")
            result = purchasing_link_page.get_success_result(purchasing_link_page.create_purchase_order_success)
            log.info(f"创建采购订单成功，结果：{result}")
            assert "新增成功" in result
            purchasing_link_page.get_shot("create_purchase_order_success.png")

            # 审核采购订单
            purchasing_link_page.purchase_audit("Ikun")
            res = purchasing_link_page.fd_element(purchasing_link_page.tag_order_audited).text
            log.info(f"审核采购订单成功，结果：{res}")
            assert "已审核" in res
            purchasing_link_page.get_shot("purchase_audit_success.png")

            # 供应商发货
            purchasing_link_page.supplier_deliver("逆丰慢运", "SF9876543210", "15")
            res = purchasing_link_page.fd_element(purchasing_link_page.tag_order_shipped).text
            log.info(f"供应商发货成功，结果：{res}")
            assert "已发货" in res
            purchasing_link_page.get_shot("supplier_deliver_success.png")

            purchasing_link_page.receive_purchase()
            res = purchasing_link_page.fd_element(purchasing_link_page.tag_order_received).text
            log.info(f"收货采购订单成功，结果：{res}")
            assert "已收货" in res
            purchasing_link_page.get_shot("receive_purchase_success.png")

            purchasing_link_page.stock_in_purchase("华东主仓")
            res = purchasing_link_page.fd_element(purchasing_link_page.tag_order_stock_in_success).text
            log.info(f"生成采购入库单成功，结果：{res}")
            assert "已入库" in res
            purchasing_link_page.get_shot("stock_in_purchase_success.png")



        except Exception as e:
            log.error("采购链路失败")
            PurchasingLinkPage(login_brower).get_shot("purchase_link_failed.png")
            raise e
