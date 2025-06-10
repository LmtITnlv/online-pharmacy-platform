from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from decimal import Decimal

# Create your views here.

@login_required
def order_create(request):
    cart = Cart(request)
    
    # 检查购物车是否为空
    if len(cart) == 0:
        messages.warning(request, '您的购物车为空，请先添加商品')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()
            
            # 添加购物车中商品到订单
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # 清空购物车
            cart.clear()
            
            messages.success(request, '订单创建成功！')
            return redirect('orders:order_detail', order_id=order.id)
    else:
        # 尝试从用户资料中预填表单
        initial_data = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = {
                'full_name': profile.full_name,
                'address': profile.address,
                'phone': profile.phone
            }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'orders/order_create.html', {
        'form': form,
        'cart': cart
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
