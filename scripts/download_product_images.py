import os
import django
import requests
import tempfile
from django.core.files import File

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_platform.settings')
django.setup()

from products.models import Product

# 创建media目录（如果不存在）
os.makedirs('media/products/samples', exist_ok=True)

# 通用药品图片URL列表（使用placeholder图片作为示例）
# 注意：在实际项目中应该使用真实药品图片
image_urls = [
    'https://via.placeholder.com/300x300.png?text=药品示例1',
    'https://via.placeholder.com/300x300.png?text=药品示例2',
    'https://via.placeholder.com/300x300.png?text=药品示例3',
    'https://via.placeholder.com/300x300.png?text=药品示例4',
    'https://via.placeholder.com/300x300.png?text=药品示例5',
    'https://via.placeholder.com/300x300.png?text=药品示例6',
]

def download_image_for_product(product, image_url, index):
    """下载图片并将其添加到产品中"""
    try:
        # 下载图片
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            print(f"无法下载图片: {image_url}")
            return False

        # 创建临时文件
        img_temp = tempfile.NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()

        # 设置文件名
        filename = f"product_{product.id}_image_{index}.png"
        
        # 将图片保存到产品
        product.image.save(filename, File(img_temp), save=True)
        print(f"为产品 '{product.name}' 添加了图片: {filename}")
        return True
    
    except Exception as e:
        print(f"为产品 '{product.name}' 添加图片时出错: {str(e)}")
        return False

# 为每个产品添加图片
products = Product.objects.filter(image='')  # 仅选择没有图片的产品
count = 0

for i, product in enumerate(products):
    # 选择图片URL（循环使用可用的图片）
    image_url = image_urls[i % len(image_urls)]
    
    # 下载并添加图片
    if download_image_for_product(product, image_url, i+1):
        count += 1

print(f"\n成功为 {count} 个产品添加了图片") 