from django.test import TestCase
from django.urls import reverse

class CoreViewsTest(TestCase):
    def test_home_view(self):
        """测试首页视图"""
        url = reverse('core:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
        # 检查页面标题是否在响应内容中
        self.assertContains(response, 'MASTER药房')
    
    def test_about_view(self):
        """测试关于我们页面视图"""
        url = reverse('core:about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
        self.assertContains(response, '关于我们')
    
    def test_contact_view(self):
        """测试联系我们页面视图"""
        url = reverse('core:contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
        self.assertContains(response, '联系我们')
