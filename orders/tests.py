from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Category, Product
from .models import Order, OrderItem
from decimal import Decimal
import uuid

class OrderModelTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        # 添加随机后缀以避免slug冲突
        self.unique_suffix1 = f"{uuid.uuid4()}"[:8]
        self.unique_suffix2 = f"{uuid.uuid4()}"[:8]
        
        # 创建用户
        self.user = User.objects.create_user(
            username=f'testuser-{self.unique_suffix1}',
            password='password',
            email='test@example.com'
        )
        
        # 创建分类和产品
        self.category = Category.objects.create(
            name=f"感冒药-{self.unique_suffix1}",
            slug=f"gan-mao-yao-{self.unique_suffix1}"
        )
        self.product1 = Product.objects.create(
            name=f"复方感冒灵-{self.unique_suffix1}",
            description="用于感冒发热",
            price=Decimal('15.50'),
            stock=100,
            category=self.category,
            slug=f"fu-fang-gan-mao-ling-{self.unique_suffix1}"
        )
        self.product2 = Product.objects.create(
            name=f"阿司匹林片-{self.unique_suffix2}",
            description="用于缓解疼痛",
            price=Decimal('9.90'),
            stock=50,
            category=self.category,
            slug=f"a-si-pi-lin-pian-{self.unique_suffix2}"
        )
        
        # 创建订单
        self.order = Order.objects.create(
            user=self.user,
            full_name='测试用户',
            address='北京市海淀区',
            phone='13800138000',
            total_price=Decimal('40.90')
        )
        
        # 创建订单项
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            price=Decimal('15.50'),
            quantity=2
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            price=Decimal('9.90'),
            quantity=1
        )
    
    def test_order_creation(self):
        """测试订单创建功能"""
        self.assertTrue(isinstance(self.order, Order))
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.full_name, '测试用户')
        self.assertEqual(self.order.status, 'pending')  # 默认状态
        self.assertEqual(self.order.total_price, Decimal('40.90'))
        self.assertEqual(self.order.__str__(), f'订单 {self.order.id}')
    
    def test_order_items(self):
        """测试订单项关联"""
        self.assertEqual(self.order.items.count(), 2)
        
        # 验证第一个订单项
        item1 = self.order.items.filter(product=self.product1).first()
        self.assertEqual(item1.product, self.product1)
        self.assertEqual(item1.price, Decimal('15.50'))
        self.assertEqual(item1.quantity, 2)
        self.assertEqual(item1.get_cost(), Decimal('31.00'))
        
        # 验证第二个订单项
        item2 = self.order.items.filter(product=self.product2).first()
        self.assertEqual(item2.product, self.product2)
        self.assertEqual(item2.price, Decimal('9.90'))
        self.assertEqual(item2.quantity, 1)
        self.assertEqual(item2.get_cost(), Decimal('9.90'))
    
    def test_order_total_calculation(self):
        """测试订单总价计算"""
        expected_total = Decimal('31.00') + Decimal('9.90')  # 第一个订单项总价 + 第二个订单项总价
        self.assertEqual(self.order.total_price, expected_total)

class OrderItemModelTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        # 添加随机后缀以避免slug冲突
        self.unique_suffix = f"{uuid.uuid4()}"[:8]
        
        # 创建用户
        self.user = User.objects.create_user(
            username=f'testuser-{self.unique_suffix}',
            password='password',
            email='test@example.com'
        )
        
        # 创建分类和产品
        self.category = Category.objects.create(
            name=f"感冒药-{self.unique_suffix}",
            slug=f"gan-mao-yao-{self.unique_suffix}"
        )
        self.product = Product.objects.create(
            name=f"复方感冒灵-{self.unique_suffix}",
            description="用于感冒发热",
            price=Decimal('15.50'),
            stock=100,
            category=self.category,
            slug=f"fu-fang-gan-mao-ling-{self.unique_suffix}"
        )
        
        # 创建订单
        self.order = Order.objects.create(
            user=self.user,
            full_name='测试用户',
            address='北京市海淀区',
            phone='13800138000',
            total_price=Decimal('31.00')
        )
        
        # 创建订单项
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal('15.50'),
            quantity=2
        )
    
    def test_order_item_creation(self):
        """测试订单项创建功能"""
        self.assertTrue(isinstance(self.order_item, OrderItem))
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.price, Decimal('15.50'))
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.__str__(), f'2个 {self.product.name}')
    
    def test_get_cost(self):
        """测试获取订单项总价功能"""
        self.assertEqual(self.order_item.get_cost(), Decimal('31.00'))
