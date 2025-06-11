from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review
from cart.forms import CartAddProductForm
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    sort = request.GET.get('sort', '')  # 获取排序参数
    search_query = request.GET.get('q', '')  # 获取搜索参数
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # 根据搜索词过滤产品
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
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
        'sort_text': sort_text,
        'search_query': search_query
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    # 获取相关产品
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    # 获取产品评价
    reviews = product.reviews.all()
    
    # 计算平均评分
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # 处理评价表单
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    review_form = ReviewForm(instance=user_review)
    
    if request.method == 'POST' and request.user.is_authenticated:
        if 'review_submit' in request.POST:
            if user_review:
                review_form = ReviewForm(request.POST, instance=user_review)
            else:
                review_form = ReviewForm(request.POST)
                
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, '您的评价已提交！')
                return redirect('products:product_detail', slug=product.slug)
    
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': review_form,
        'user_review': user_review
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    messages.success(request, '您的评价已删除！')
    return redirect('products:product_detail', slug=product_slug)
