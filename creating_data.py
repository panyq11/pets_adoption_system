import os
import django
from django.utils import timezone
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pets_adoption_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.files import File
from posts.models import Pet, PetImage, PostPetInfo, PostReview
from adoptions.models import AdoptPetInfo, AdoptionReview

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@admin.com',
        password='admin'
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")


user, created = User.objects.get_or_create(
    username="user",
    defaults={'email': 'user@user.com'}
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

pet_list = [{"pet_name":"Lucky", "status": "Available", "type": "Dog", "post_status": "Pending", "has_apply": False},
            {"pet_name":"Diasy", "status": "Available", "type": "Cat", "post_status": "Approved", "has_apply": False},
            {"pet_name":"Lisa", "status": "Available", "type": "Cat", "post_status": "Rejected", "has_apply": False},
            {"pet_name":"Coco", "status": "Available", "type": "Cat", "post_status": "Approved", "has_apply": True, "adopt_status": "Pending"},
            {"pet_name":"Milo", "status": "Adopted", "type": "Cat", "post_status": "Approved", "has_apply": True, "adopt_status": "Approved"},
            {"pet_name":"Luna", "status": "Available", "type": "Dog", "post_status": "Approved", "has_apply": True, "adopt_status": "Rejected"}]


for pet in pet_list:

    pet_instance, created = Pet.objects.get_or_create(
        name=pet["pet_name"],
        defaults={
            'sex': random.choice(["Male", "Female"]),
            'age': random.choice(["Young", "Adult"]),
            'weight': 10.0,
            'breed': random.choice(["golden", "blue", "white"]),
            'size': random.choice(["Large", "Medium", "Small"]),
            'status': pet["status"],
            'posted_by': user,
            'type': 'Cat',  # 此处类型设为 'Cat'
        }
    )

    # 2. 为 Pet 创建关联图片（假设图片文件位于脚本所在目录下的 test_images 文件夹）
    image_dir = os.path.join(os.path.dirname(__file__), 'media', 'test_images')
    i = 1
    found_any = False
    while True:
        image_filename = f"{pet['pet_name']}_{i}.jpg"
        image_path = os.path.join(image_dir, image_filename)
        if os.path.exists(image_path):
            found_any = True
            with open(image_path, 'rb') as img_file:
                PetImage.objects.create(
                    pet=pet_instance,
                    pet_image=File(img_file, name=image_filename)
                )
            i += 1
        else:
            break

    if not found_any:
        print("No image file found for:", pet["pet_name"])

    post_pet_info = PostPetInfo.objects.create(
        pet=pet_instance,
        user=user,
        email=user.email,
        home_type=random.choice(["Apartment", "House", "Townhouse", "Farm/Rural"]),
        home_ownership=random.choice(["Own", "Rent", "Living with parents", "Other"]),
        has_other_pets='No other pets',
        has_children=random.choice(['0','1','2','3','4','5']),  # '0' 表示没有孩子
        experience_with_pets='I have raised pets before.',
        reason_for_fostering='I love animals and want to give them a better home.',
        pet_passport=random.randint(100000, 999999),
        vaccinated='Yes',
        status=pet["post_status"],
        review_time = timezone.now(),
    )

    post_review = PostReview.objects.create(
        pet=pet_instance,
        username=user,         # 申请人
        operator_username=reviewer,  # 审核人（管理员）
        status=pet["post_status"]

    )

    print(f"{pet['pet_name']} created successfully!")

    if pet["has_apply"]:
        pet_instance.status = pet["status"]
        pet_instance.save()

        adopt_info = AdoptPetInfo.objects.create(
            pet=pet_instance,
            user=user,
            operator=reviewer,
            home_type=random.choice(["Apartment", "House", "Townhouse", "Farm/Rural"]),
            home_ownership=random.choice(["Own", "Rent", "Living with parents", "Other"]),
            has_landlord_permission=True,
            has_other_pets='No other pets',
            has_children=random.choice(['0','1','2','3','4','5']),
            experience_with_pets='I have experience with pets from my previous pet ownership.',
            reason_for_adoption='I love animals and want to provide a loving home.',
        )

        # 6. 创建 AdoptionReview（领养申请审核记录）
        adoption_review = AdoptionReview.objects.create(
            adopt_info=adopt_info,
            pet=pet_instance,
            adopter_username=user,
            operator_username=reviewer,
            status=pet["adopt_status"],
            review_time=timezone.now(),
        )

        print(f"Adoption data for pet '{pet['pet_name']}' created successfully!")


print("All test data created successfully!")

