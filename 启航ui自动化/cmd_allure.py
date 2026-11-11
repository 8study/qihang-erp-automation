import os
# 离线测试报告
run_cmd="allure generate ./report -o ./new_report --clean"
# allure generate  生成allure报告
# ./report  测试报告目录
# -o ./new_report  输出html的报告到新的报告目录
# --clean  清理旧的报告目录

os.system(run_cmd)  #运行终端命令
