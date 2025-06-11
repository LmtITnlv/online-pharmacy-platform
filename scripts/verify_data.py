import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_platform.settings')
django.setup()

from products.models import Category, Product
from django.core.exceptions import ValidationError
from django.db.models import Count

def check_categories():
    """检查所有分类是否完整"""
    print("\n===== 分类检查 =====")
    categories = Category.objects.all()
    
    if not categories.exists():
        print("❌ 错误: 没有任何分类")
        return False
    
    print(f"✅ 共有 {categories.count()} 个分类")
    
    # 检查每个分类是否有slug
    for category in categories:
        if not category.slug:
            print(f"❌ 错误: 分类 '{category.name}' 没有slug")
            return False
    
    print("✅ 所有分类都有slug")
    
    # 检查重复的slug
    duplicate_slugs = Category.objects.values('slug').annotate(count=Count('slug')).filter(count__gt=1)
    if duplicate_slugs.exists():
        print(f"❌ 错误: 发现重复的分类slug: {', '.join([item['slug'] for item in duplicate_slugs])}")
        return False
    
    print("✅ 所有分类slug都是唯一的")
    return True

def check_products():
    """检查所有产品是否完整"""
    print("\n===== 产品检查 =====")
    products = Product.objects.all()
    
    if not products.exists():
        print("❌ 错误: 没有任何产品")
        return False
    
    print(f"✅ 共有 {products.count()} 个产品")
    
    # 检查每个产品是否有slug
    for product in products:
        if not product.slug:
            print(f"❌ 错误: 产品 '{product.name}' 没有slug")
            return False
    
    print("✅ 所有产品都有slug")
    
    # 检查重复的slug
    duplicate_slugs = Product.objects.values('slug').annotate(count=Count('slug')).filter(count__gt=1)
    if duplicate_slugs.exists():
        print(f"❌ 错误: 发现重复的产品slug: {', '.join([item['slug'] for item in duplicate_slugs])}")
        return False
    
    print("✅ 所有产品slug都是唯一的")
    
    # 检查每个产品是否有图片
    products_without_image = Product.objects.filter(image='')
    if products_without_image.exists():
        print(f"❌ 错误: 有 {products_without_image.count()} 个产品没有图片")
        for product in products_without_image:
            print(f"  - {product.name}")
        return False
    
    print("✅ 所有产品都有图片")
    
    # 检查产品是否有有效的价格
    products_without_valid_price = Product.objects.filter(price__lte=0)
    if products_without_valid_price.exists():
        print(f"❌ 错误: 有 {products_without_valid_price.count()} 个产品价格不正确")
        for product in products_without_valid_price:
            print(f"  - {product.name}: ¥{product.price}")
        return False
    
    print("✅ 所有产品都有有效的价格")
    
    # 检查产品是否有分类
    products_without_category = Product.objects.filter(category=None)
    if products_without_category.exists():
        print(f"❌ 错误: 有 {products_without_category.count()} 个产品没有分类")
        for product in products_without_category:
            print(f"  - {product.name}")
        return False
    
    print("✅ 所有产品都有分类")
    return True

def check_relationships():
    """检查分类和产品的关系"""
    print("\n===== 关系检查 =====")
    
    # 检查每个分类是否有产品
    categories_without_products = Category.objects.annotate(product_count=Count('products')).filter(product_count=0)
    if categories_without_products.exists():
        print(f"⚠️ 警告: 有 {categories_without_products.count()} 个分类没有任何产品:")
        for category in categories_without_products:
            print(f"  - {category.name}")
    else:
        print("✅ 所有分类都有产品")
    
    # 计算每个分类的产品数量
    print("\n各分类产品数量:")
    for category in Category.objects.annotate(product_count=Count('products')):
        print(f"  - {category.name}: {category.product_count} 个产品")
    
    return True

if __name__ == "__main__":
    print("\n====================")
    print("药品数据完整性检查")
    print("====================")
    
    categories_ok = check_categories()
    products_ok = check_products()
    relationships_ok = check_relationships()
    
    print("\n====================")
    if categories_ok and products_ok and relationships_ok:
        print("✅ 数据检查通过，所有数据完整!")
    else:
        print("❌ 数据检查未通过，请修复上述问题!")
    print("====================\n") 