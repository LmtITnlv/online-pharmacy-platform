from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        """
        初始化购物车
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # 如果会话中没有购物车则创建一个空购物车
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def add(self, product, quantity=1, override_quantity=False):
        """
        添加商品到购物车或更新数量
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        """
        保存购物车到会话
        """
        self.session.modified = True
    
    def remove(self, product):
        """
        从购物车中移除商品
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """
        遍历购物车中的商品并从数据库获取商品
        """
        product_ids = self.cart.keys()
        # 获取购物车内的商品并添加到购物车
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        计算购物车中的商品数量
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        计算购物车中商品的总价
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """
        清空购物车
        """
        # 清空购物车字典
        self.cart = {}
        # 删除会话中的购物车并重新设置为空字典
        self.session[settings.CART_SESSION_ID] = {}
        self.save() 