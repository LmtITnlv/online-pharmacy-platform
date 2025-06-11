from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField('分类名称', max_length=100)
    slug = models.SlugField('URL别名', unique=True)
    description = models.TextField('描述', blank=True)
    
    class Meta:
        verbose_name = '药品分类'
        verbose_name_plural = '药品分类'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField('药品名称', max_length=200)
    slug = models.SlugField('URL别名', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='分类')
    image = models.ImageField('药品图片', upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField('详细描述')
    price = models.DecimalField('价格', max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField('库存', default=0)
    available = models.BooleanField('是否上架', default=True)
    prescription_required = models.BooleanField('是否处方药', default=False)
    created = models.DateTimeField('创建日期', auto_now_add=True)
    updated = models.DateTimeField('更新日期', auto_now=True)
    
    class Meta:
        verbose_name = '药品'
        verbose_name_plural = '药品'
        ordering = ('-created',)
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1星'),
        (2, '2星'),
        (3, '3星'),
        (4, '4星'),
        (5, '5星'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='药品')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name='用户')
    rating = models.IntegerField('评分', choices=RATING_CHOICES)
    comment = models.TextField('评价内容')
    created = models.DateTimeField('创建时间', auto_now_add=True)
    
    class Meta:
        verbose_name = '药品评价'
        verbose_name_plural = '药品评价'
        ordering = ('-created',)
        # 确保每个用户只能对一个产品评价一次
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f'{self.user.username}对{self.product.name}的评价'
