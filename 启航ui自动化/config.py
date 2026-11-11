import os

import pymysql
from faker import Faker

# 获取项目路径
PATH=os.path.dirname(__file__)

# 项目地址
BASE_URL="http://127.0.0.1:88"

# 数据库配置（用例前置数据清理用）
DB_HOST="127.0.0.1"
DB_PORT=3306
DB_USER="root"
DB_PASSWORD=""
DB_DATABASE="qihang-erp"


faker=Faker(locale="zh_CN")
NAME=faker.name()
PHONE=faker.phone_number()
CARD=faker.ssn()

conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                                    password=DB_PASSWORD, database=DB_DATABASE, charset="utf8mb4")

# 手动添加店铺商品数据清理
ADD_SHOP_GOODS_SQLS = [
        "DELETE FROM oms_shop_order_item WHERE shop_order_id IN (SELECT id FROM oms_shop_order WHERE order_id = 'SO20260929001')",
        "DELETE FROM oms_shop_order WHERE order_id = 'SO20260929001'",
        "DELETE FROM o_order_item WHERE order_id IN (SELECT id FROM o_order WHERE order_num = 'SO20260929001')",
        "DELETE FROM o_order WHERE order_num = 'SO20260929001'",
        "DELETE FROM oms_shop_goods_sku WHERE shop_goods_id IN (SELECT id FROM oms_shop_goods WHERE spu_code = 'SHOP-TEST-20260929-001')",
        "DELETE FROM oms_shop_goods WHERE spu_code = 'SHOP-TEST-20260929-001'",
        # 后端 addGoods 按平台商品ID全局查重，清掉历史遗留的 P001（含旧商家编码 20260923 的数据）
        "DELETE FROM oms_shop_goods_sku WHERE product_id = 'P001'",
        "DELETE FROM oms_shop_goods WHERE product_id = 'P001'",
    ]

# 新建入库单+执行入库+出库数据清理（子表先删，单表DELETE+子查询）
# 入库 localStockIn 写库存表+批次表，出库 stockOut 按 FIFO 扣批次 current_qty 和总库存——
# 两者对库存的影响都通过"按 SKU 删行重建"一次性复位（手动建单批次 pur_id=0 与期初无法区分，
# 且 CATE-UITEST-001-C-001 是 UI 测试专用 SKU，库存全为测试产物，删行重建比 UPDATE 减法幂等）
STOCK_IN_SQLS = [
        "DELETE FROM o_goods_inventory_batch WHERE sku_id IN (SELECT id FROM o_goods_sku WHERE sku_code = 'CATE-UITEST-001-C-001')",
        "DELETE FROM o_goods_inventory WHERE sku_id IN (SELECT id FROM o_goods_sku WHERE sku_code = 'CATE-UITEST-001-C-001')",
        # 出库单：实体无@TableName注解，MyBatis-Plus 按类名映射到 erp_stock_out（wms_stock_out 是同构空表），
        # 主表单号列 out_num、明细外键 entry_id
        "DELETE FROM erp_stock_out_item WHERE entry_id IN (SELECT id FROM erp_stock_out WHERE out_num = 'CK20260929001')",
        "DELETE FROM erp_stock_out WHERE out_num = 'CK20260929001'",
        "DELETE FROM erp_stock_in_item WHERE stock_in_id IN (SELECT id FROM erp_stock_in WHERE stock_in_num = 'RK20260929001')",
        "DELETE FROM erp_stock_in WHERE stock_in_num = 'RK20260929001'",
    ]

# 采购承运商（快递公司）数据清理
# 后端 /erp/logistics/add 直接 save 无查重，重复执行会堆重复数据；
# 页面无删除入口，按名称/编码删历史数据保证用例可反复执行（单表，无子表）
PURCHASE_SUPPLIER_SQLS = [
        "DELETE FROM erp_purchase_logistics WHERE code = 'nf10086' OR name = '逆丰慢运'",
    ]

# 采购订单数据清理（子表先查后删，主表DELETE+子查询）
# 单号是后端 "PUR"+时间戳 自动生成，无法按固定单号删；改按测试专用 SKU 定位——
# 只删包含 CATE-UITEST-001-C-001 的采购单，不影响供应商下其他订单。
# 收货/入库链路共写四张表，删除顺序必须保证子查询还能查到：
# 1.入库单明细（stock_in_id挂入库单）→ 2.入库单主表（source_id=采购单id，趁采购子表还在）→
# 3.发货记录表（每次发货插行）→ 4.采购主表 → 5.采购子表。
# 入库单按 source_id 链路删而非 sku_code：老订单手动生成的入库单已入过库（库存已加），
# 按 sku_code 删会误伤其明细造成库存不一致。均不写库存表
PURCHASE_ORDER_SQLS = [
        "DELETE FROM erp_stock_in_item WHERE stock_in_id IN (SELECT id FROM erp_stock_in WHERE source_id IN (SELECT order_id FROM erp_purchase_order_item WHERE spec_num = 'CATE-UITEST-001-C-001'))",
        "DELETE FROM erp_stock_in WHERE source_id IN (SELECT order_id FROM erp_purchase_order_item WHERE spec_num = 'CATE-UITEST-001-C-001') AND stock_in_type = 1",
        "DELETE FROM erp_purchase_order_ship WHERE order_id IN (SELECT order_id FROM erp_purchase_order_item WHERE spec_num = 'CATE-UITEST-001-C-001')",
        "DELETE FROM erp_purchase_order WHERE id IN (SELECT order_id FROM erp_purchase_order_item WHERE spec_num = 'CATE-UITEST-001-C-001')",
        "DELETE FROM erp_purchase_order_item WHERE spec_num = 'CATE-UITEST-001-C-001'",
    ]

# 售后台账数据清理
# 售后单号 RF20260929001 为测试专用，按单号删即可。添加售后只写 o_refund_after_sale 一张表；
# 后续"退货确认"还会生成退货入库单——单号是 THRK-日期-时间戳 随机生成，
# 但 source_no = 售后单号 可确定性关联（stock_in_type=2 退货入库），
# 删除顺序：入库明细 → 入库主表 → 售后记录本体。退货确认本身不改库存表
AFTER_SALE_SQLS = [
        "DELETE FROM erp_stock_in_item WHERE stock_in_id IN (SELECT id FROM erp_stock_in WHERE source_no = 'RF20260929001' AND stock_in_type = 2)",
        "DELETE FROM erp_stock_in WHERE source_no = 'RF20260929001' AND stock_in_type = 2",
        "DELETE FROM o_refund_after_sale WHERE refund_num = 'RF20260929001'",
    ]

# 角色+用户（RBAC）数据清理
# 新增角色写 sys_role + sys_role_menu（角色-菜单授权关系），
# 新增用户写 sys_user + sys_user_role（用户-角色关联）。
# 页面虽有删除入口，但用例要求可反复执行，前置按唯一标识清库更干净：
# 角色按权限字符 uiTestRole 定位、用户按账号 uitest 定位。
# 删除顺序必须先清关系表（子查询依赖 sys_role / sys_user 还在），再删主表
ROLE_USER_SQLS = [
        "DELETE FROM sys_role_menu WHERE role_id IN (SELECT role_id FROM sys_role WHERE role_key = 'uiTestRole')",
        "DELETE FROM sys_user_role WHERE user_id IN (SELECT user_id FROM sys_user WHERE user_name = 'uitest') OR role_id IN (SELECT role_id FROM sys_role WHERE role_key = 'uiTestRole')",
        "DELETE FROM sys_user WHERE user_name = 'uitest'",
        "DELETE FROM sys_role WHERE role_key = 'uiTestRole'",
    ]