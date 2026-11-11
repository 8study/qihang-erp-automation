from base.base import BasePage
from config import *
from locators_helper import is_visible, sub_menu
from page.role_user_link import RoleUserLinkPage
from script import log

ROLE_NAME = "UITestRole"
ROLE_KEY = "uiTestRole"
ROLE_SORT = "10"
NICK_NAME = "UI测试用户"
PHONE = "13900139000"
EMAIL = "uitest@example.com"
USER_NAME = "uitest"
PASSWORD = ""
SEX = "男"
REMARK = "UI自动化"


class TestRoleUserLink:
    def setup_method(self):
        # 前置清理：删掉上一轮创建的角色（含菜单授权关系）和用户（含角色关联）
        BasePage.sql_clean(ROLE_USER_SQLS, conn)
        log.info("前置SQL清理完成：已清空测试角色 uiTestRole 与测试用户 uitest")

    def teardown_method(self):
        conn.close()

    def test_role_user_rbac(self, login_brower):
        try:
            role_user_page = RoleUserLinkPage(login_brower)

            # 新增角色
            role_user_page.add_role(ROLE_NAME, ROLE_KEY, ROLE_SORT, REMARK)
            result = role_user_page.get_success_result(role_user_page.create_role_success)
            log.info(f"新增角色成功，结果：{result}")
            assert "新增成功" in result
            role_user_page.get_shot("add_role_success.png")

            # 新增用户：关联"UI测试角色"
            role_user_page.add_user(NICK_NAME, PHONE, EMAIL, USER_NAME,
                                    PASSWORD, SEX, ROLE_NAME, REMARK)
            result = role_user_page.get_success_result(role_user_page.create_user_success)
            log.info(f"新增用户成功，结果：{result}")
            assert "新增成功" in result
            role_user_page.get_shot("add_user_success.png")

            # 新用户登录验证 RBAC：只显示被授权的"商品管理"，其余菜单不可见
            # 不再调用 close_onboarding：新手引导的"本会话已弹过"标记存在 sessionStorage，
            # 同标签页跨刷新保留，fixture 里 admin 登录时已标记，此处弹窗必然不会再弹，
            # 再调一次只会白等满它固定的 10 秒轮询
            role_user_page.relogin(USER_NAME, PASSWORD)
            assert is_visible(role_user_page, role_user_page.sidebar_goods, timeout=10), \
                "已授权的商品管理菜单未显示"
            # 商品管理已确认可见 => 侧边栏已渲染完成，其余菜单就是确定不存在，
            # 越权探测用 0.5 秒即可（is_visible 对不存在的元素会耗满整个 timeout）
            for unauthorized in ("订单管理", "售后管理", "采购管理", "发货管理", "仓库管理", "系统设置"):
                assert not is_visible(role_user_page, sub_menu(unauthorized), timeout=0.5), \
                    f"越权菜单可见：{unauthorized}"
            log.info("RBAC 校验通过：仅商品管理菜单可见")
            role_user_page.get_shot("rbac_menu_success.png")

        except Exception as e:
            log.error(f"角色-用户-RBAC链路失败：{e}")
            RoleUserLinkPage(login_brower).get_shot("role_user_link_failed.png")
            raise e
