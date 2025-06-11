from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    sort = request.GET.get('sort', '')  # 获取排序参数
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # 根据排序参数对产品进行排序
    if sort == 'price_asc':
        products = products.order_by('price')  # 价格从低到高
        sort_text = '价格从低到高'
    elif sort == 'price_desc':
        products = products.order_by('-price')  # 价格从高到低
        sort_text = '价格从高到低'
    elif sort == 'newest':
        products = products.order_by('-created')  # 最新上架
        sort_text = '最新上架'
    else:
        sort_text = '默认排序'  # 默认排序
    
    # 为每个产品创建一个添加到购物车的表单
    for product in products:
        product.cart_form = CartAddProductForm()
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'sort': sort,
        'sort_text': sort_text
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'products/product_detail.html', context)
