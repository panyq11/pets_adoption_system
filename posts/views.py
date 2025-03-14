from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Pet, PetImage, PostReview
from .forms import PetForm, PetImageForm



def my_posts(request):
    return render(request, 'posts/myPosts.html')


def post_pet(request):
    if request.method == "POST":
        pet_form = PetForm(request.POST)
        image_form = PetImageForm(request.POST, request.FILES)
        if pet_form.is_valid() and image_form.is_valid():
            # 保存宠物基本信息
            pet = pet_form.save(commit=False)
            pet.posted_by = request.user
            pet.status = 'Pending'  # 标记为待审核
            pet.save()

            # 获取上传的图片（注意 HTML 中 input 的 name 必须和这里保持一致）
            images = request.FILES.getlist('petPhotos')
            # 限制最多上传 6 张图片
            if len(images) > 6:
                images = images[:6]
            for image in images:
                PetImage.objects.create(pet=pet, pet_image=image)

            print(f"✅ 宠物 {pet.name} 数据存入数据库，ID: {pet.pet_id}")
            return redirect(reverse('posts/postReview.html', args=[pet.pet_id]))


    else:
        pet_form = PetForm()
        image_form = PetImageForm()

    context = {
        'pet_form': pet_form,
        'image_form': image_form,
    }
    return render(request, 'posts/postPet.html', context)




def review_status(request):
    return render(request, 'posts/postReview.html')