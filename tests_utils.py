"""
测试工具模块 - 提供测试相关的实用函数和fixture
"""
from django.contrib.auth.models import User
from django.test.client import Client
from products.models import Category, Product, Review
from users.models import Profile
from orders.models import Order, OrderItem
from decimal import Decimal
import uuid
import random

def generate_unique_slug(base_name):
    """生成唯一的基于名称的slug，添加随机数防止冲突"""
    random_suffix = f"-{str(uuid.uuid4())[:8]}-{random.randint(1000, 9999)}"
    return f"{base_name}{random_suffix}"

def create_test_user(username="testuser", password="password", email="test@example.com"):
    """创建测试用户及其资料"""
    # 添加随机后缀确保唯一性
    unique_username = f"{username}-{str(uuid.uuid4())[:8]}"
    user = User.objects.create_user(username=unique_username, password=password, email=email)
    profile = Profile.objects.create(
        user=user,
        full_name='测试用户',
        phone='13800138000',
        address='北京市海淀区'
    )
    return user, profile

def create_test_category(name="测试分类", description="测试分类描述"):
    """创建测试分类"""
    # 添加随机后缀确保唯一性
    unique_name = generate_unique_slug(name)
    category = Category.objects.create(name=unique_name, description=description)
    return category

def create_test_product(category, name="测试产品", price=Decimal('19.90')):
    """创建测试产品"""
    # 添加随机后缀确保唯一性
    unique_name = generate_unique_slug(name)
    product = Product.objects.create(
        name=unique_name,
        description="测试产品描述",
        price=price,
        stock=100,
        category=category
    )
    return product

def create_test_review(product, user, rating=5, comment="测试评价"):
    """创建测试评价"""
    review = Review.objects.create(
        product=product,
        user=user,
        rating=rating,
        comment=comment
    )
    return review

def create_test_order(user):
    """创建测试订单"""
    order = Order.objects.create(
        user=user,
        full_name='测试用户',
        address='北京市海淀区',
        phone='13800138000',
        total_price=Decimal('0.00')
    )
    return order

def create_test_order_item(order, product, quantity=1):
    """创建测试订单项"""
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price,
        quantity=quantity
    )
    # 更新订单总价
    order.total_price += product.price * quantity
    order.save()
    return order_item

def authenticated_client(user=None):
    """返回已经认证的客户端"""
    if not user:
        user, _ = create_test_user()
    
    client = Client()
    client.login(username=user.username, password='password')
    return client, user 