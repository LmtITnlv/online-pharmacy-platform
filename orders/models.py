from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    ORDER_STATUS = (
        ('pending', '待付款'),
        ('paid', '已付款'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    full_name = models.CharField('收件人姓名', max_length=100)
    address = models.TextField('收货地址')
    phone = models.CharField('联系电话', max_length=15)
    created = models.DateTimeField('创建日期', auto_now_add=True)
    updated = models.DateTimeField('更新日期', auto_now=True)
    status = models.CharField('订单状态', max_length=20, choices=ORDER_STATUS, default='pending')
    total_price = models.DecimalField('总价', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        ordering = ('-created',)
        
    def __str__(self):
        return f'订单 {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='药品')
    price = models.DecimalField('购买价格', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('数量', default=1)
    
    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项'
        
    def __str__(self):
        return f'{self.quantity}个 {self.product.name}'
    
    def get_cost(self):
        return self.price * self.quantity
