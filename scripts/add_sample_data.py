import os
import django
import random
from decimal import Decimal
import uuid

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_platform.settings')
django.setup()

from products.models import Category, Product
from django.utils.text import slugify

# 清除现有数据
Product.objects.all().delete()
Category.objects.all().delete()

# 创建药品分类
categories = [
    {
        'name': '感冒用药',
        'description': '用于感冒、流感等症状的药品，包括退热、止咳、祛痰等'
    },
    {
        'name': '消化系统',
        'description': '用于胃部不适、消化不良、胃痛等症状的药品'
    },
    {
        'name': '心脑血管',
        'description': '用于心脑血管疾病的预防和治疗的药品'
    },
    {
        'name': '抗生素',
        'description': '各类抗生素药品，用于细菌感染等'
    },
    {
        'name': '维生素和营养品',
        'description': '各类维生素、矿物质补充剂和营养保健品'
    },
    {
        'name': '皮肤用药',
        'description': '用于皮肤问题的外用药物和护理产品'
    },
]

# 添加分类
created_categories = []
for cat_data in categories:
    # 手动创建唯一的slug
    base_slug = slugify(cat_data['name'])
    # 确保slug不为空
    if not base_slug:
        # 使用拼音或英文别名，或者直接使用uuid
        base_slug = f"category-{uuid.uuid4().hex[:8]}"
    
    # 检查是否已存在同名分类
    existing_category = Category.objects.filter(name=cat_data['name']).first()
    if existing_category:
        print(f"分类已存在: {cat_data['name']}")
        created_categories.append(existing_category)
        continue
    
    # 检查是否有相同的slug
    if Category.objects.filter(slug=base_slug).exists():
        # 如果slug已存在，添加随机后缀
        unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
    else:
        unique_slug = base_slug
    
    # 创建新分类
    category = Category(
        name=cat_data['name'],
        slug=unique_slug,
        description=cat_data['description']
    )
    category.save()
    created_categories.append(category)
    print(f"创建分类: {category.name}, slug: {category.slug}")

# 药品数据
products = [
    # 感冒用药
    {
        'name': '布洛芬缓释胶囊',
        'category_name': '感冒用药',
        'description': '用于缓解轻至中度疼痛如头痛、关节痛、偏头痛、牙痛、肌肉痛、神经痛、痛经。也用于普通感冒或流行性感冒引起的发热。',
        'price': Decimal('25.80'),
        'stock': 100,
        'prescription_required': False
    },
    {
        'name': '感冒灵颗粒',
        'category_name': '感冒用药',
        'description': '解热镇痛，用于感冒引起的头痛、发热、鼻塞、流涕、咽痛等。',
        'price': Decimal('15.50'),
        'stock': 150,
        'prescription_required': False
    },
    {
        'name': '复方感冒片',
        'category_name': '感冒用药',
        'description': '适用于缓解普通感冒及流行性感冒引起的发热、头痛、四肢酸痛、打喷嚏、流鼻涕、鼻塞、咽痛等症状。',
        'price': Decimal('12.80'),
        'stock': 200,
        'prescription_required': False
    },
    {
        'name': '小儿感冒颗粒',
        'category_name': '感冒用药',
        'description': '疏风解表，清热解毒。用于小儿风热感冒，症见发热、头痛、咳嗽、口渴、咽喉肿痛。',
        'price': Decimal('22.50'),
        'stock': 80,
        'prescription_required': False
    },
    
    # 消化系统
    {
        'name': '奥美拉唑肠溶胶囊',
        'category_name': '消化系统',
        'description': '适用于胃溃疡、十二指肠溃疡、应激性溃疡、反流性食管炎和卓-艾综合征（胃泌素瘤）。',
        'price': Decimal('38.60'),
        'stock': 120,
        'prescription_required': True
    },
    {
        'name': '蒙脱石散',
        'category_name': '消化系统',
        'description': '用于成人及儿童急、慢性腹泻，亦可用于消化不良引起的腹泻。',
        'price': Decimal('28.90'),
        'stock': 150,
        'prescription_required': False
    },
    {
        'name': '吗丁啉片',
        'category_name': '消化系统',
        'description': '适用于消化不良，腹胀，嗳气，恶心，呕吐，腹部胀痛。',
        'price': Decimal('32.50'),
        'stock': 90,
        'prescription_required': True
    },
    
    # 心脑血管
    {
        'name': '阿司匹林肠溶片',
        'category_name': '心脑血管',
        'description': '用于预防血栓形成，如预防心肌梗死、脑血栓形成，也用于治疗不稳定型心绞痛。',
        'price': Decimal('15.60'),
        'stock': 200,
        'prescription_required': True
    },
    {
        'name': '辛伐他汀片',
        'category_name': '心脑血管',
        'description': '本品适用于高胆固醇血症及冠心病。',
        'price': Decimal('42.80'),
        'stock': 100,
        'prescription_required': True
    },
    {
        'name': '银杏叶片',
        'category_name': '心脑血管',
        'description': '活血化瘀通络。用于瘀血阻络引起的胸痹心痛、中风、半身不遂、舌强语謇；冠心病稳定型心绞痛、脑梗死见上述证候者。',
        'price': Decimal('36.50'),
        'stock': 180,
        'prescription_required': False
    },
    
    # 抗生素
    {
        'name': '阿莫西林胶囊',
        'category_name': '抗生素',
        'description': '适用于敏感菌所致的上呼吸道感染、下呼吸道感染、泌尿生殖道感染及皮肤软组织感染等。',
        'price': Decimal('18.50'),
        'stock': 150,
        'prescription_required': True
    },
    {
        'name': '头孢克洛干混悬剂',
        'category_name': '抗生素',
        'description': '适用于敏感菌引起的急性扁桃体炎、咽炎、中耳炎、鼻窦炎、下呼吸道感染、尿路感染及皮肤软组织感染等。',
        'price': Decimal('45.80'),
        'stock': 80,
        'prescription_required': True
    },
    
    # 维生素和营养品
    {
        'name': '复合维生素B片',
        'category_name': '维生素和营养品',
        'description': '用于预防和治疗维生素B1、B2、B6、烟酰胺缺乏症。',
        'price': Decimal('26.80'),
        'stock': 200,
        'prescription_required': False
    },
    {
        'name': '钙片',
        'category_name': '维生素和营养品',
        'description': '补充钙质，预防骨质疏松症。',
        'price': Decimal('32.50'),
        'stock': 180,
        'prescription_required': False
    },
    {
        'name': '维生素C片',
        'category_name': '维生素和营养品',
        'description': '用于预防和治疗维生素C缺乏症，如坏血病等。',
        'price': Decimal('12.80'),
        'stock': 250,
        'prescription_required': False
    },
    
    # 皮肤用药
    {
        'name': '复方酮康唑软膏',
        'category_name': '皮肤用药',
        'description': '用于皮肤真菌感染，如手足癣、体癣、股癣、花斑癣等。',
        'price': Decimal('28.50'),
        'stock': 120,
        'prescription_required': False
    },
    {
        'name': '湿毒清片',
        'category_name': '皮肤用药',
        'description': '清热利湿，解毒止痒。用于湿热蕴蓄所致的湿疹、脂溢性皮炎、慢性荨麻疹。',
        'price': Decimal('34.80'),
        'stock': 100,
        'prescription_required': False
    },
    {
        'name': '马应龙麝香痔疮膏',
        'category_name': '皮肤用药',
        'description': '活血化瘀，清热解毒，收敛止痛。用于内痔出血，肿痛，外痔肿痛。',
        'price': Decimal('22.80'),
        'stock': 150,
        'prescription_required': False
    }
]

# 清除所有现有药品（可选）
# Product.objects.all().delete()

# 添加药品
for prod_data in products:
    try:
        # 获取对应分类
        category = Category.objects.get(name=prod_data['category_name'])
        
        # 检查是否已存在同名药品
        existing_product = Product.objects.filter(name=prod_data['name']).first()
        if existing_product:
            print(f"药品已存在: {prod_data['name']}")
            continue
        
        # 创建唯一的slug
        base_slug = slugify(prod_data['name'])
        # 确保slug不为空或过短
        if not base_slug or len(base_slug) <= 2:
            # 使用拼音或英文别名，或者直接使用药品名称的拼音首字母加uuid
            base_slug = f"product-{uuid.uuid4().hex[:8]}"
        
        if Product.objects.filter(slug=base_slug).exists():
            # 如果slug已存在，添加随机后缀
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        else:
            unique_slug = base_slug
        
        # 创建产品
        product = Product(
            name=prod_data['name'],
            slug=unique_slug,
            category=category,
            description=prod_data['description'],
            price=prod_data['price'],
            stock=prod_data['stock'],
            prescription_required=prod_data['prescription_required']
        )
        product.save()
        print(f"创建药品: {product.name}, slug: {product.slug}")
        
    except Category.DoesNotExist:
        print(f"分类不存在: {prod_data['category_name']}")
    except Exception as e:
        print(f"添加药品时出错: {prod_data['name']} - {str(e)}")

print("数据添加完成！") 