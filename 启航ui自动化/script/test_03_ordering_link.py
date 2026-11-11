import pymysql
from base.base import BasePage
from config import *
from page.ordering_link import OrderingLink
from script import log


class TestOrderingLink:
    # S3 相关数据的清理 SQL（子表先删；商家编码与用例传入的 SHOP-TEST-20260929-001 保持一致）

    def setup_method(self):
        # 用例自建数据库连接并前置清理，保证 P001 / 商家编码无残留

        BasePage.sql_clean(ADD_SHOP_GOODS_SQLS, conn)
        log.info("前置SQL清理完成：已清空订单 SO20260929001 与店铺商品 SHOP-TEST-20260929-001 相关数据")

    def teardown_method(self):
        # 关闭本用例创建的连接；不做数据清理，保留本次添加的商品供页面查看，
        # 重复执行由 setup_method 的前置清理保证
        conn.close()

    def test_ordering_link(self, login_brower):
        try:
            ordering_link = OrderingLink(login_brower)
            # 添加店铺商品
            ordering_link.add_shop_goods("启航淘宝旗舰店", "UI测试店铺商品", "SHOP-TEST-20260929-001", "P001",
                                         "10", "20")
            success_result = ordering_link.get_success_result(ordering_link.shop_goods_save_success)
            log.info(f"添加店铺商品成功，返回结果：{success_result}")
            assert "保存成功" in success_result
            ordering_link.get_shot("add_shop_goods_success.png")

            # 添加店铺订单
            ordering_link.add_shop_orders("SO20260929001", "启航淘宝旗舰店", "张三", "13800138000",
                                          "广东省", "深圳市", "南山区", "科技园路1号", "2")
            success_result = ordering_link.get_success_result(ordering_link.order_save_success)
            log.info(f"添加店铺订单成功，返回结果：{success_result}")
            assert "订单创建成功" in success_result
            ordering_link.get_shot("add_shop_orders_success.png")

            # 推送订单
            ordering_link.push_orders()
            log.info("推送订单成功")
            ordering_link.get_shot("push_orders_success.png")

            # 手动发货
            ordering_link.hand_delivery("SF1234567890")
            success_result = ordering_link.get_success_result(ordering_link.hand_delivery_success)
            log.info(f"手动发货成功，返回结果：{success_result}")
            assert "发货成功" in success_result
            ordering_link.get_shot("hand_delivery_success.png")

        except Exception as e:
            log.error("订单链路失败")
            OrderingLink(login_brower).get_shot("ordering_failed.png")
            raise e
