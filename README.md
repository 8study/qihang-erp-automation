# 启航电商 ERP 自动化测试

基于 **Pytest** 的 UI 自动化与接口自动化测试项目，覆盖启航电商 ERP 的核心业务流程：登录、商品、订单、库存、采购、售后、系统权限（RBAC）与个人中心。

## 项目结构

```
.
├── 启航ui自动化/                 # Web UI 自动化（Selenium + Page Object）
│   ├── base/                    # 页面基类：元素操作、截图、SQL 数据清理
│   ├── page/                    # 页面对象（登录、商品、订单、库存、采购、售后、角色用户）
│   ├── script/                  # UI 测试用例
│   ├── data/                    # 登录用例数据（JSON）
│   ├── config.py                # 环境地址、数据库配置、前置清理 SQL
│   ├── locators_helper.py       # 通用元素定位封装
│   ├── conftest.py              # 浏览器与登录前置 fixture
│   ├── pytest.ini
│   └── cmd_allure.py            # Allure 报告生成
└── 启航接口自动化/               # 接口自动化（Pytest + Excel 数据驱动）
    ├── base/                    # 全局变量存储（Token 等）
    ├── testcases/               # 接口测试用例
    ├── utils/                   # 用例解析、HTTP/JDBC 断言、Excel 读取
    ├── data/                    # 测试用例 Excel
    ├── config.py                # 接口地址、数据库配置
    ├── conftest.py              # 会话级登录前置
    ├── pytest.ini
    └── cmd_allure.py            # Allure 报告生成
```

## 技术栈

| 分类 | 技术 |
| --- | --- |
| 测试框架 | Pytest |
| UI 自动化 | Selenium、Page Object 模式、Edge WebDriver |
| 接口自动化 | Requests、JSONPath 断言、Excel 数据驱动（openpyxl + Jinja2） |
| 数据校验 | PyMySQL（前置清理与 SQL 断言） |
| 测试报告 | Allure |
| 其他 | Faker（测试数据生成）、Logging |

## 环境准备

1. 本地启动被测系统：
   - UI 地址：`http://127.0.0.1:88`
   - 接口地址：`http://127.0.0.1:6149/api`
2. 准备 MySQL 数据库 `qihang-erp`，并保证用例中的测试数据表存在。
3. 安装依赖：

```bash
pip install pytest selenium allure-pytest pymysql requests openpyxl jsonpath jinja2 faker
```

4. 安装 Edge 浏览器与对应 WebDriver。
5. 安装 Allure 命令行工具（用于生成 HTML 报告）。

## 配置说明

为了避免泄露敏感信息，仓库中的密码已替换为空值，运行前请在本地补齐：

| 文件 | 配置项 |
| --- | --- |
| `启航ui自动化/config.py` | `DB_PASSWORD` |
| `启航接口自动化/config.py` | `DB_PASSWORD` |
| `启航ui自动化/conftest.py` | admin 登录密码 |
| `启航ui自动化/data/login_data.json` | 登录用例密码 |
| `启航接口自动化/data/启航电商测试用例.xlsx` | 用例中的登录/用户密码 |

## 运行测试

### UI 自动化

```bash
cd 启航ui自动化
pytest                          # 执行全部 UI 用例
python cmd_allure.py            # 生成 Allure HTML 报告到 new_report/
```

### 接口自动化

```bash
cd 启航接口自动化
pytest                          # 执行全部接口用例
pytest --feature 登录           # 只执行指定模块
python cmd_allure.py            # 生成 Allure HTML 报告
```

## 用例覆盖

- **UI**：登录校验、商品基础资料、店铺与订单、库存出入库、采购全流程、售后退货、角色-用户 RBAC 权限
- **接口**：登录鉴权、商品分类与商品新增、店铺商品、订单创建、推单出库、手动发货、采购、售后、数据清理、系统管理与权限、个人中心

## 说明

本项目仅用于自动化测试学习与实践，测试数据均为测试环境数据，敏感凭据已移除。
