from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages  # ✅ 用于存储成功消息
from .models import Pet, PetImage, PostReview, PostPetInfo
from .forms import PetForm, PetImageForm, PostPetInfoForm
from django.contrib.auth import get_user_model

User = get_user_model()


def my_posts(request):
    # ✅ 只查询当前用户发布的宠物
    user_pets = Pet.objects.filter(posted_by=request.user).order_by('-created_at')

    context = {'pet_list': user_pets}
    return render(request, 'posts/myPosts.html', context)


def delete_pet(request, pet_id):
    """ 删除宠物 API """
    if request.method == "POST":
        pet = get_object_or_404(Pet, pet_id=pet_id)

        # ✅ 限制只能删除自己发布的宠物
        if request.user != pet.posted_by:
            return JsonResponse({"message": "Unauthorized"}, status=403)

        pet.delete()
        return JsonResponse({"message": "Deleted successfully"}, status=200)

    return JsonResponse({"message": "Invalid request"}, status=400)




def post_pet(request):
    if request.method == "POST":
        pet_form = PetForm(request.POST)
        image_form = PetImageForm(request.POST, request.FILES)
        post_info_form = PostPetInfoForm(request.POST)  # ✅ **新增寄养信息表单**

        print("📸 Debugging request.FILES: ", request.FILES)  # ✅ 终极调试

        if pet_form.is_valid() and image_form.is_valid() and post_info_form.is_valid():

            # 确保 `posted_by` 不是匿名用户
            if request.user.is_authenticated:
                user = request.user  # ✅ 如果用户已登录，使用当前用户
                print(f"✅ Authenticated user: {user.username} (ID: {user.id})")  # **调试信息**
            else:
                user = User.objects.filter(id=1).first()
                if not user:
                    print("❌ Default user ID=1 does not exist! Creating a new one...")
                    user = User.objects.create(
                        id=1,
                        username="default_user",
                        email="default@example.com",
                        user_type="User",
                        status="Active",
                    )
                print(f"✅ Using default user: {user.username} (ID: {user.id})")  # **调试信息**

            # **🐶 创建宠物对象**
            pet = pet_form.save(commit=False)
            pet.posted_by = request.user
            pet.status = 'Pending'  # 默认审核中
            pet.save()

            # **📸 存储宠物图片**
            images = request.FILES.getlist('pet_image')[:6]  # 限制 6 张

            for image in images:
                pet_image = PetImage.objects.create(pet=pet, pet_image=image)
                print(f"✅ Uploaded image URL: {pet_image.pet_image.url}")  # 终端打印调试信息

            # **🏠 存储额外的寄养信息**
            post_info = post_info_form.save(commit=False)
            # 获取email字段并存储到数据库
            email_from_form = request.POST.get('email')
            if email_from_form:
                post_info.email = email_from_form

            post_info.pet = pet
            post_info.user = request.user  # **记录发布人的信息**
            post_info.email = user.email if user.is_authenticated else "default@example.com"

            post_info.save()

            # ✅ **终端调试**
            print(f"✅ 宠物 {pet.name} 已存入数据库，ID: {pet.pet_id}")
            print(f"📧 发布人 Email: {post_info.email}")

            # ✅ **弹窗提示**
            messages.success(request, f"🎉 Your pet '{pet.name}' has been posted successfully! Pending approval.")

            return redirect('postPet')  # **刷新当前页面，防止重复提交**
        else:
            print("❌ 表单错误：", pet_form.errors, image_form.errors, post_info_form.errors)
            messages.error(request, "Post failed! Please try again.")  # ✅ Fail

    else:
        pet_form = PetForm()
        image_form = PetImageForm()
        post_info_form = PostPetInfoForm()

    return render(request, 'posts/postPet.html', {
        'pet_form': pet_form,
        'image_form': image_form,
        'post_info_form': post_info_form  # ✅ **传递寄养信息表单**
    })




def review_status(request):

    # 过滤当前用户发布的宠物审核信息
    post_list = PostPetInfo.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'post_list': post_list
    }
    return render(request, 'posts/postReview.html', context)