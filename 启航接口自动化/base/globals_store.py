# -*- coding: utf-8 -*-
"""
全局共享变量存储。

整个测试会话中只有这一个 GLOBAL_VAR 字典对象：
  - conftest.py 会话级前置登录后，通过这个字典写入 TOKEN
  - test_001_login.py 里 global_var 与它指向同一个对象，因此能收到 token
  - 各用例通过 json/jdbc 提取的中间值（如 categoryId、attrId）也会累积进来

模板渲染时把 GLOBAL_VAR 传给 jinja2 render，即可将
{{TOKEN}}、{{categoryId}}、{{attrId}} 等占位符替换为实际值。
"""
GLOBAL_VAR = {}