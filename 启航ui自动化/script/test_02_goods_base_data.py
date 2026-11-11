from conftest import login_brower
from page.goods_base_data import GoodsBaseData
from script import log


class TestGoodsBaseData:

    def test_add_goods_base(self, login_brower, goods_cleanup):
        try:
            goods_base_data = GoodsBaseData(login_brower)
            goods_base_data.add_goods_category("CATE-UITEST-001", "UI测试分类", "UI自动化", "1")
            goods_base_data.get_shot("add_goods_category_success.png")

            goods_base_data.add_goods_attribute("颜色", "1")
            goods_base_data.get_shot("add_goods_attribute_success.png")

            goods_base_data.enter_attribute_value()
            goods_base_data.add_attribute_value("红色", "1")
            goods_base_data.add_attribute_value("蓝色", "2")
            goods_base_data.get_shot("add_goods_attribute_value_success.png")

            goods_base_data.add_brand("测试品牌B", "B001")
            goods_base_data.get_shot("add_goods_brand_success.png")

            goods_base_data.add_goods("UI测试分类", "测试品牌B", "Ikun练习供应商",
                                      "UI测试商品", ["红M", "蓝L"], "10", "20")
            result = goods_base_data.get_success_result(goods_base_data.success_result)
            log.info(f"商品库列表可查，商品：{result}")
            assert "UI测试商品" in result
            goods_base_data.get_shot("add_goods_success.png")

        except Exception as e:
            log.error("商品基础数据添加失败")
            GoodsBaseData(login_brower).get_shot("add_goods_base_failed.png")
            raise e
