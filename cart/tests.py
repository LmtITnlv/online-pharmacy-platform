from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from products.models import Category, Product
from .cart import Cart
from decimal import Decimal
import uuid

class CartTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        # 添加随机后缀以避免slug冲突
        self.unique_suffix1 = f"{uuid.uuid4()}"[:8]
        self.unique_suffix2 = f"{uuid.uuid4()}"[:8]
        
        # 创建请求工厂
        self.factory = RequestFactory()
        
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
        
        # 创建请求并设置会话
        self.request = self.factory.get('/')
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(self.request)
        self.request.session.save()
        
        # 初始化购物车
        self.cart = Cart(self.request)
    
    def test_add_product(self):
        """测试添加商品到购物车"""
        # 添加一个产品
        self.cart.add(product=self.product1)
        
        # 检查购物车中的产品数量
        self.assertEqual(len(self.cart), 1)
        
        # 添加更多相同的产品
        self.cart.add(product=self.product1, quantity=2)
        # 现在应该有3个相同的产品
        product_id = str(self.product1.id)
        self.assertEqual(self.cart.cart[product_id]['quantity'], 3)
    
    def test_add_multiple_products(self):
        """测试添加多个不同商品到购物车"""
        # 添加两种不同的产品
        self.cart.add(product=self.product1, quantity=2)
        self.cart.add(product=self.product2, quantity=1)
        
        # 检查购物车中的产品总数
        self.assertEqual(len(self.cart), 3)
        
        # 检查购物车中的项目数
        self.assertEqual(len(list(self.cart)), 2)
    
    def test_remove_product(self):
        """测试从购物车中移除商品"""
        # 先添加产品
        self.cart.add(product=self.product1)
        self.cart.add(product=self.product2)
        
        # 确认购物车中有两种产品
        self.assertEqual(len(list(self.cart)), 2)
        
        # 移除一种产品
        self.cart.remove(self.product1)
        
        # 确认购物车中只剩一种产品
        self.assertEqual(len(list(self.cart)), 1)
        
        # 确认剩下的产品是产品2
        for item in self.cart:
            self.assertEqual(item['product'], self.product2)
    
    def test_get_total_price(self):
        """测试计算购物车总价"""
        # 添加产品
        self.cart.add(product=self.product1, quantity=2)  # 2 * 15.50 = 31.00
        self.cart.add(product=self.product2, quantity=1)  # 1 * 9.90 = 9.90
        
        # 计算期望总价
        expected_total = Decimal('31.00') + Decimal('9.90')  # 40.90
        
        # 检查总价是否正确
        self.assertEqual(self.cart.get_total_price(), expected_total)
    
    def test_clear_cart(self):
        """测试清空购物车"""
        # 先添加产品
        self.cart.add(product=self.product1)
        self.cart.add(product=self.product2)
        
        # 确认购物车中有产品
        self.assertTrue(len(self.cart) > 0)
        
        # 清空购物车
        self.cart.clear()
        
        # 确认购物车为空
        self.assertEqual(len(self.cart), 0)
