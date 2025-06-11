import os
import django
import random
from PIL import Image, ImageDraw, ImageFont
import io
from django.core.files.base import ContentFile

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_platform.settings')
django.setup()

from products.models import Product

# 创建media目录（如果不存在）
os.makedirs('media/products/samples', exist_ok=True)

# 颜色列表，用于生成不同的占位图片
colors = [
    (220, 53, 69),   # 红色
    (40, 167, 69),   # 绿色
    (0, 123, 255),   # 蓝色
    (255, 193, 7),   # 黄色
    (111, 66, 193),  # 紫色
    (23, 162, 184),  # 青色
]

def create_placeholder_image(product, index):
    """为产品创建占位图片"""
    try:
        # 图片尺寸
        width, height = 300, 300
        
        # 随机选择背景颜色
        bg_color = colors[index % len(colors)]
        
        # 创建图片对象
        image = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(image)
        
        # 绘制产品名称文本（简化处理，不处理字体问题）
        text = product.name
        # 如果有PIL的ImageFont，可以加载字体
        # 但这里简化处理，直接绘制文本
        text_position = (width // 2 - 50, height // 2)
        draw.text(text_position, text, fill=(255, 255, 255))
        
        # 将图片转换为文件对象
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        
        # 设置文件名
        filename = f"product_{product.id}_image_{index}.jpg"
        
        # 将图片保存到产品
        product.image.save(filename, ContentFile(img_io.getvalue()), save=True)
        print(f"为产品 '{product.name}' 创建了图片: {filename}")
        return True
    
    except Exception as e:
        print(f"为产品 '{product.name}' 创建图片时出错: {str(e)}")
        return False

# 为每个产品添加图片
products = Product.objects.filter(image='')  # 仅选择没有图片的产品
count = 0

for i, product in enumerate(products):
    # 创建并添加图片
    if create_placeholder_image(product, i+1):
        count += 1

print(f"\n成功为 {count} 个产品添加了图片") 