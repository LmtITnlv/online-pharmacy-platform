from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Category, Product, Review
from decimal import Decimal
import uuid

class CategoryModelTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        # 添加随机后缀以避免slug冲突
        self.unique_suffix = str(uuid.uuid4())[:8]
        self.name = f"感冒药-{self.unique_suffix}"
        self.category = Category.objects.create(
            name=self.name, 
            description="治疗感冒相关药物"
        )
    
    def test_category_creation(self):
        """测试分类创建功能"""
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(self.category.__str__(), self.name)
        # 检查slug是否被正确设置，但不硬编码预期值
        self.assertTrue(self.category.slug)
        self.assertEqual(self.category.slug, slugify(self.name))
    
    def test_category_slug_generation(self):
        """测试分类自动生成 slug"""
        unique_name = f"解热镇痛-{str(uuid.uuid4())[:8]}"
        category = Category.objects.create(name=unique_name)
        self.assertEqual(category.slug, slugify(unique_name))

class ProductModelTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        # 添加随机后缀以避免slug冲突
        self.unique_suffix = str(uuid.uuid4())[:8]
        self.category_name = f"感冒药-{self.unique_suffix}"
        self.product_name = f"复方感冒灵-{self.unique_suffix}"
        
        self.category = Category.objects.create(name=self.category_name)
        self.product = Product.objects.create(
            name=self.product_name,
            description="用于感冒发热",
            price=Decimal('15.50'),
            stock=100,
            category=self.category
        )
    
    def test_product_creation(self):
        """测试产品创建功能"""
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), self.product_name)
        self.assertEqual(self.product.price, Decimal('15.50'))
        self.assertEqual(self.product.stock, 100)
        self.assertTrue(self.product.available)
        self.assertFalse(self.product.prescription_required)
        # 检查slug是否被正确设置
        self.assertTrue(self.product.slug)
        self.assertEqual(self.product.slug, slugify(self.product_name))
    
    def test_product_slug_generation(self):
        """测试产品自动生成 slug"""
        unique_name = f"阿司匹林片-{str(uuid.uuid4())[:8]}"
        product = Product.objects.create(
            name=unique_name,
            description="用于缓解疼痛",
            price=Decimal('9.90'),
            stock=50,
            category=self.category
        )
        self.assertEqual(product.slug, slugify(unique_name))
    
    def test_get_average_rating(self):
        """测试获取平均评分功能"""
        user = User.objects.create_user(username=f'testuser-{self.unique_suffix}', password='password')
        
        # 创建评价
        Review.objects.create(product=self.product, user=user, rating=4, comment="很好")
        
        # 测试平均分
        self.assertEqual(self.product.get_average_rating(), 4)
        
        # 再添加一个评价
        user2 = User.objects.create_user(username=f'testuser2-{self.unique_suffix}', password='password')
        Review.objects.create(product=self.product, user=user2, rating=2, comment="一般")
        
        # 重新测试平均分
        self.assertEqual(self.product.get_average_rating(), 3)

class ReviewModelTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        # 添加随机后缀以避免slug冲突
        self.unique_suffix = str(uuid.uuid4())[:8]
        
        self.user = User.objects.create_user(
            username=f'testuser-{self.unique_suffix}', 
            password='password'
        )
        self.category = Category.objects.create(name=f"感冒药-{self.unique_suffix}")
        self.product = Product.objects.create(
            name=f"复方感冒灵-{self.unique_suffix}",
            description="用于感冒发热",
            price=Decimal('15.50'),
            stock=100,
            category=self.category
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="非常好的药品"
        )
    
    def test_review_creation(self):
        """测试评价创建功能"""
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "非常好的药品")
        expected_str = f"{self.user.username}对{self.product.name}的评价"
        self.assertEqual(self.review.__str__(), expected_str)
