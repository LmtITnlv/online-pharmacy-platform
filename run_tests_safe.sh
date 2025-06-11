#!/bin/bash

# 设置Python路径确保能找到项目模块
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 告知Django使用测试配置
export DJANGO_SETTINGS_MODULE=pharmacy_platform.settings

# 运行测试前清除Python缓存文件
echo "=== 清除Python缓存文件 ==="
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# 在测试模式下运行Django测试 - 这会自动使用一个临时测试数据库
echo "=== 运行单元测试 (每个应用分开测试) ==="
python manage.py test core.tests
python manage.py test products.tests
python manage.py test users.tests
python manage.py test orders.tests
python manage.py test cart.tests

echo ""
echo "=== 测试完成 ===" 