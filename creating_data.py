import os
import django

# 在导入任何 Django 模型之前先配置环境变量和调用 django.setup()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pets_adoption_system.settings')
django.setup()

from posts.models import Pet, PetImage
from django.core.files import File
from django.contrib.auth import get_user_model
from django.conf import settings

def create_test_data():
    # 获取自定义用户模型
    User = get_user_model()  # 返回 account.User（前提是你在 settings.py 中设置了 AUTH_USER_MODEL = 'account.User'）
    user, created = User.objects.get_or_create(username="testuser")
    if created:
        user.set_password("testpass")
        user.save()

    # 创建宠物记录
    pet1 = Pet.objects.create(
        name="Buddy",
        sex="Male",
        age=3,
        weight=15.0,
        breed="Golden Retriever",
        size="Large",
        status="Available",
        posted_by=user,
        type="Cat"
    )

    pet2 = Pet.objects.create(
        name="Kitty",
        sex="Female",
        age=2,
        weight=4.5,
        breed="Siamese",
        size="Small",
        status="Available",
        posted_by=user,
        type="Cat"
    )

    # 创建宠物图片记录
    images = [
        (pet1, 'image1.jpg', 'buddy.jpg'),
        (pet2, 'image2.jpg', 'kitty.jpg'),
    ]

    for pet, src_name, target_name in images:
        file_path = os.path.join(settings.MEDIA_ROOT, 'post_pet', src_name)
        try:
            with open(file_path, 'rb') as img_file:
                PetImage.objects.create(
                    pet=pet,
                    pet_image=File(img_file, name=target_name)
                )
            print(f"成功为 {pet.name} 创建图片 {target_name}")
        except FileNotFoundError:
            print(f"文件 {file_path} 不存在！")

if __name__ == '__main__':
    create_test_data()
