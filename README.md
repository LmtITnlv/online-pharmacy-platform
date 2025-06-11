# MASTER药房在线平台

![MASTER药房](static/images/logo.png)

MASTER药房是一个专业的线上购药平台，为用户提供优质药品和专业药学服务。平台采用响应式设计，支持PC和移动设备访问，提供丰富的交互体验。

## 功能特点

- **全面的药品管理**: 支持多品类药品分类和详情展示
- **智能搜索系统**: 快速查找所需药品
- **用户账户管理**: 个人信息、订单历史和收货地址管理
- **购物车功能**: 方便的商品选购和结算流程
- **订单系统**: 完整的下单、支付、配送和订单跟踪
- **药师在线咨询**: 专业用药指导和咨询服务
- **健康资讯**: 提供药品相关知识和健康信息
- **响应式界面**: 适配各种设备尺寸的美观界面
- **安全支付**: 支持多种安全支付方式

## 技术栈

- **后端**: Django 5.2
- **数据库**: SQLite (开发环境)，支持PostgreSQL (生产环境)
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **响应式设计**: 移动优先的响应式界面
- **动画效果**: AOS (Animate On Scroll)

## 安装及配置

### 环境要求

- Python 3.9+
- pip (Python包管理工具)

### 安装步骤

1. **克隆代码库**

```bash
git clone https://github.com/yourusername/online-pharmacy-platform.git
cd online-pharmacy-platform
```

2. **创建并激活虚拟环境**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **应用数据库迁移**

```bash
python manage.py migrate
```

5. **创建超级用户(可选)**

```bash
python manage.py createsuperuser
```

6. **运行开发服务器**

```bash
python manage.py runserver
```

现在，您可以通过访问 [http://localhost:8000/](http://localhost:8000/) 来查看网站。

## 项目结构

```
online-pharmacy-platform/
├── core/               # 核心应用：基本页面和共享功能
├── products/           # 产品应用：药品和分类管理
├── users/              # 用户应用：用户验证和资料管理
├── orders/             # 订单应用：订单处理和管理
├── cart/               # 购物车应用：购物车功能
├── static/             # 静态文件(CSS, JS, 图片)
├── media/              # 用户上传的媒体文件(药品图片等)
├── templates/          # HTML模板
└── pharmacy_platform/  # 项目设置和主URL配置
```

## 测试

项目包含完整的单元测试套件，您可以使用以下命令运行测试:

```bash
# 运行所有测试
./run_tests_safe.sh

# 运行特定应用的测试
python manage.py test products

# 生成测试覆盖率报告
./run_tests_coverage.sh
```

## 贡献

欢迎提交问题报告、功能请求或代码贡献。请在提交前确保代码遵循PEP 8风格指南并通过测试。

## 许可证

该项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 联系方式

如有问题或建议，请通过以下方式联系我们:

- 邮箱: contact@masterpharmacy.com
- 网站: https://www.masterpharmacy.com
- 地址: 北京市海淀区中关村大街1号 