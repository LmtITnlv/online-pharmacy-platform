#!/bin/bash

# 安装测试依赖
pip install coverage

# 清除旧的覆盖率数据
coverage erase

echo "=== 运行测试覆盖率分析 ==="
# 排除虚拟环境、迁移文件和其他不必要的文件
coverage run --source='.' \
  --omit="venv/*,*/migrations/*,*/tests.py,*/tests/*,*/__pycache__/*,*/settings.py,*/wsgi.py,*/asgi.py,manage.py" \
  manage.py test core products users orders cart

# 生成报告
echo "=== 生成覆盖率报告 ==="
coverage report

echo ""
echo "=== 生成HTML覆盖率报告 ==="
coverage html

echo ""
echo "测试覆盖率HTML报告已生成在 htmlcov/ 目录中"
echo "请在浏览器中打开 htmlcov/index.html 查看详细报告" 