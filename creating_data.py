import os
import django

# 配置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pets_adoption_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.files import File
from posts.models import Pet, PetImage, PostPetInfo, PostReview
from adoptions.models import AdoptPetInfo, AdoptionReview

User = get_user_model()

# 1. 创建测试用户（普通用户）和管理员
user, created = User.objects.get_or_create(
    username="user",
    defaults={'email': 'testuser@example.com'}
)
if created:
    user.set_password("user")
    user.save()

reviewer, created = User.objects.get_or_create(
    username="reviewer",
    defaults={'email': 'admin@example.com', 'user_type': 'Admin'}
)
if created:
    reviewer.set_password("reviewer")
    reviewer.save()

pet_list = ["tuantuan", "guyu", "gancao", "baolu"]

for pet_name in pet_list:
    # 1. 创建或获取 Pet 实例
    pet_instance, created = Pet.objects.get_or_create(
        name=pet_name,
        defaults={
            'sex': 'Male',
            'age': 'Young',  # 年龄字段为 CharField，可选 'Young' 或 'Adult'
            'weight': 15.0,
            'breed': 'Golden Retriever',
            'size': 'Large',
            'status': 'Available',
            'posted_by': user,
            'type': 'Cat',  # 此处类型设为 'Cat'
        }
    )

    # 2. 为 Pet 创建关联图片（假设图片文件位于脚本所在目录下的 test_images 文件夹）
    image_path = os.path.join(os.path.dirname(__file__), 'media/test_images', f'{pet_name}.jpg')
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            PetImage.objects.create(
                pet=pet_instance,
                pet_image=File(img_file, name=f'{pet_name}.jpg')
            )
    else:
        print("Image file not found at:", image_path)

    post_pet_info = PostPetInfo.objects.create(
        pet=pet_instance,
        user=user,
        email=user.email,
        home_type='Apartment',
        home_ownership='Own',
        has_other_pets='No other pets',
        has_children='1',  # '0' 表示没有孩子
        experience_with_pets='I have raised pets before.',
        reason_for_fostering='I love animals and want to give them a better home.',
        pet_passport='Available',
        vaccinated='Yes',
        status='Approved',
    )

    post_review = PostReview.objects.create(
        pet_id=pet_instance,
        username=user,         # 申请人
        operator_username=reviewer,  # 审核人（管理员）
        status='Pending'
    )

    print(f"Test data for pet '{pet_name}' created successfully!")

    # 5. 创建 AdoptPetInfo（用户提交的领养申请记录）
    adopt_info = AdoptPetInfo.objects.create(
        pet=pet_instance,
        user=user,
        operator=reviewer,
        home_type='Apartment',
        home_ownership='Own',
        has_landlord_permission=True,
        has_other_pets='No other pets',
        has_children='1',
        experience_with_pets='I have experience with pets from my previous pet ownership.',
        reason_for_adoption='I love animals and want to provide a loving home.',
        pet_passport='Available'
    )

    # 6. 创建 AdoptionReview（领养申请审核记录）
    adoption_review = AdoptionReview.objects.create(
        pet=pet_instance,
        adopter_username=user,
        operator_username=reviewer,
        status='Pending'
    )

    print(f"Adoption data for pet '{pet_name}' created successfully!")

print("All test data created successfully!")

