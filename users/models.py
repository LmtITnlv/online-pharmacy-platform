from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField('手机号码', max_length=15, blank=True)
    address = models.TextField('收货地址', blank=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        
    def __str__(self):
        return f'{self.user.username}的资料'
