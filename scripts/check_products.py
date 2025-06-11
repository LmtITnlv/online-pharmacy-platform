import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_platform.settings')
django.setup()

from products.models import Category, Product

# 打印分类和产品信息
print("\n===== 药品分类和产品信息 =====")
for category in Category.objects.all():
    print(f"\n分类: {category.name}")
    print(f"描述: {category.description}")
    print(f"URL别名: {category.slug}")
    print(f"产品数量: {category.products.count()}")
    
    print("\n该分类下的产品:")
    for product in category.products.all():
        print(f" - {product.name}")
        print(f"   价格: ¥{product.price}")
        print(f"   库存: {product.stock}")
        print(f"   是否处方药: {'是' if product.prescription_required else '否'}")
        print(f"   URL别名: {product.slug}")
        print()

# 统计信息
total_categories = Category.objects.count()
total_products = Product.objects.count()
prescription_products = Product.objects.filter(prescription_required=True).count()
non_prescription_products = Product.objects.filter(prescription_required=False).count()

print("\n===== 统计信息 =====")
print(f"分类总数: {total_categories}")
print(f"药品总数: {total_products}")
print(f"处方药数量: {prescription_products}")
print(f"非处方药数量: {non_prescription_products}") 