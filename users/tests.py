from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile
from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm

class ProfileModelTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(
            username='testuser', 
            password='password',
            email='test@example.com'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            full_name='测试用户',
            phone='13800138000',
            address='北京市海淀区'
        )
    
    def test_profile_creation(self):
        """测试用户资料创建功能"""
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(self.profile.__str__(), "testuser的资料")
        self.assertEqual(self.profile.full_name, "测试用户")
        self.assertEqual(self.profile.phone, "13800138000")
        self.assertEqual(self.profile.address, "北京市海淀区")

class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        """测试用户注册表单有效性"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': '新用户',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        """测试用户注册表单无效性（缺少必填字段）"""
        form_data = {
            'username': 'newuser',
            # 缺少 email
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)
    
    def test_password_mismatch(self):
        """测试密码不匹配情况"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complex_password123',
            'password2': 'different_password',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('password2' in form.errors)

class UserProfileFormTest(TestCase):
    def test_valid_form(self):
        """测试用户资料表单有效性"""
        form_data = {
            'phone': '13900139000',
            'address': '上海市浦东新区',
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

class UserViewsTest(TestCase):
    def setUp(self):
        """设置测试数据"""
        self.user = User.objects.create_user(
            username='testuser', 
            password='password',
            email='test@example.com'
        )
        self.register_url = reverse('users:register')
        self.login_url = reverse('users:login')
        
    def test_register_view_get(self):
        """测试注册页面 GET 请求"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        
    def test_register_view_post_success(self):
        """测试注册成功"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': '新用户',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(User.objects.count(), 2)  # 之前的 testuser + 新注册的用户
        self.assertEqual(Profile.objects.count(), 1)  # 应该为新用户创建资料
        
    def test_login_view(self):
        """测试登录视图"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        
        # 测试登录功能
        data = {
            'username': 'testuser',
            'password': 'password',
        }
        response = self.client.post(self.login_url, data)
        # 登录成功后应该重定向
        self.assertEqual(response.status_code, 302)
