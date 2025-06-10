from django.shortcuts import render
from products.models import Product, Category

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True)[:8]
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'core/home.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
