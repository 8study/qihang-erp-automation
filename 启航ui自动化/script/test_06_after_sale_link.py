from base.base import BasePage
from config import *
from page.after_sale_link import AfterSaleLinkPage
from script import log


class TestAfterSaleLink:
    def setup_method(self):
        # 前置清理：删掉上一轮创建的售后记录（含退货确认生成的退货入库单）
        BasePage.sql_clean(AFTER_SALE_SQLS, conn)
        log.info("前置SQL清理完成：已清空售后记录 RF20260929001")

    def teardown_method(self):
        conn.close()

    def test_add_after_sale(self,login_brower):
        try:
            after_sale_link_page = AfterSaleLinkPage(login_brower)
            # 添加售后记录
            after_sale_link_page.add_after_sale("退货","RF20260929001","SO20260929001","UI测试店铺商品",
                                                "CATE-UITEST-001-C-001","1","质量问题")
            result = after_sale_link_page.get_success_result(after_sale_link_page.create_after_sale_success)
            log.info(f"添加售后记录成功:{result}")
            assert "添加成功" in result
            after_sale_link_page.get_shot("add_after_sale_success.png")

            # 退货确认
            after_sale_link_page.confirm_return("逆丰慢运","SF0001","退货入库")
            result = after_sale_link_page.get_success_result(after_sale_link_page.return_confirm_success)
            log.info(f"退货确认成功:{result}")
            assert "处理成功" in result
            after_sale_link_page.get_shot("return_confirm_success.png")


        except Exception as e:
            log.info(f"售后链路失败:{e}")
            AfterSaleLinkPage(login_brower).get_shot("after_sale_link_failed.png")
            raise e
